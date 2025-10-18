import os, sys, re, uuid
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict
from qdrant_client import QdrantClient

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from back.logging_config import logger

# берём функции и конфиг из вашего загрузчика
from support_files.load_qdrant import get_embeddings_local, QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME

MIN_THRESHOLD = 0.70
DEFAULT_THRESHOLD = max(float(os.getenv("THRESHOLD", "0.75")), MIN_THRESHOLD)
TOP_K_DEFAULT = int(os.getenv("TOP_K", "5"))
MAX_TOP_K = 10

TOXIC_RE = re.compile(r"\b(идиот|дурак|туп(ой|ица)|сука|бл(я|)(т|д)|мразь|ненавижу|убью)\b|расстрел|угрожаю|повеш",
                      re.I)
INJ_RE = re.compile(r"(ignore previous|игнорируй предыдущее|system prompt|curl|http://|https://)", re.I)

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
COLL = os.getenv("QDRANT_COLLECTION", COLLECTION_NAME)

app = FastAPI(title="RAG via Qdrant (RoSBERTa)")


class Req(BaseModel):
    text: str
    top_k: int = TOP_K_DEFAULT
    threshold: float = DEFAULT_THRESHOLD


def sanitize(text: str) -> str:
    t = INJ_RE.sub(" ", text or "")
    return re.sub(r"\s+", " ", t).strip()


@app.get("/health")
def health():
    try:
        info = client.get_collection(COLL)
        return {"ok": True, "collection": COLL, "vectors": info.vectors_count}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/rag/select")
def select(a: Req, request: Request):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    if TOXIC_RE.search(a.text or ""):
        raise HTTPException(400, "Токсичный запрос отклонён.")

    q = sanitize(a.text)
    if not q:
        raise HTTPException(400, "Пустой запрос.")

    top_k = min(max(1, a.top_k), MAX_TOP_K)
    thr = max(a.threshold, MIN_THRESHOLD)

    try:
        qvec = get_embeddings_local(q, mode="query")  # вектор запроса
        res = client.search(
            collection_name=COLL,
            query_vector=qvec,
            limit=top_k,
            score_threshold=thr,
            with_payload=True,
            with_vectors=False,
        )

        cands = [{
            "source": r.payload.get("url") or r.payload.get("doc_id") or str(r.id),
            "snippet": r.payload.get("text", ""),
            "score": float(r.score)
        } for r in res]

        if not cands:  # запасной поиск без порога
            res2 = client.search(collection_name=COLL, query_vector=qvec, limit=top_k, with_payload=True)
            cands = [{
                "source": r.payload.get("url") or r.payload.get("doc_id") or str(r.id),
                "snippet": r.payload.get("text", ""),
                "score": float(r.score)
            } for r in res2]

        max_score = max([c["score"] for c in cands], default=0.0)
        eligible = [c for c in cands if c["score"] >= thr]
        passed = bool(max_score >= thr)
        coverage = round(len(eligible) / max(1, top_k), 2)

    except Exception as e:
        logger.error(f"[{rid}] Qdrant search error: {e}")
        raise HTTPException(500, "Ошибка поиска в Qdrant")

    logger.info(f"[{rid}] top_k={top_k} thr={thr} max={round(max_score, 3)} passed={passed}")
    return {
        "query": q,
        "top_k": top_k,
        "threshold": thr,
        "candidates": cands,
        "eligible_contexts": eligible,
        "max_score": round(max_score, 3),
        "coverage": coverage,
        "passed": passed
    }
