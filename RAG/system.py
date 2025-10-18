import os, sys, json, re, uuid
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#логгер
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
try:
    from back.logging_config import logger
except Exception as e:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("rag")
    logger.warning(f"Fallback logger: cannot import back.logging_config: {e}")

#безопасность
MIN_THRESHOLD = 0.70
DEFAULT_THRESHOLD = float(os.getenv("THRESHOLD", "0.75"))
DEFAULT_THRESHOLD = max(DEFAULT_THRESHOLD, MIN_THRESHOLD)
TOP_K_DEFAULT = int(os.getenv("TOP_K", "5"))
MAX_TOP_K = 10

TOXIC_PATTERNS = [
    r"\b(идиот|дурак|туп(ой|ица)|сука|бл(я|)(т|д)|мразь|ненавижу|убью)\b",
    r"расстрел|угрожаю|повеш",
]
TOXIC_RE = re.compile("|".join(TOXIC_PATTERNS), re.IGNORECASE)

INJECTION_RE = re.compile(
    r"(игнорируй предыдущее|ignore previous|системный промпт|system prompt|"
    r"выполни команду|execute|curl|powershell|http://|https://)",
    re.IGNORECASE
)

#данные
docs = []
kb_path = os.path.join(PROJECT_ROOT, "data", "ingest.ndjson")
try:
    with open(kb_path, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
                if (d.get("text") or "").strip():
                    docs.append(d)
            except Exception as e:
                logger.error(f"Bad NDJSON line: {e}")
except FileNotFoundError:
    logger.error(f"KB file not found: {kb_path}")

if not docs:
    logger.error("KB is empty — /rag/select will return 503")

def build_index(items):
    texts = [it["text"] for it in items]
    vec = TfidfVectorizer(analyzer="word", ngram_range=(1,2), min_df=1).fit(texts)
    mat = vec.transform(texts)
    return vec, mat

IDX_ALL = build_index(docs) if docs else None

# FastAPI
app = FastAPI(title="rag-select-tfidf (secure, no domains)")

class Req(BaseModel):
    text: str
    top_k: int = TOP_K_DEFAULT
    threshold: float = DEFAULT_THRESHOLD

@app.middleware("http")
async def request_id_mw(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.req_id = rid
    logger.info(f"[{rid}] RAG -> {request.url.path}")
    try:
        resp = await call_next(request)
        logger.info(f"[{rid}] RAG <- {request.url.path} {resp.status_code}")
        return resp
    except Exception as e:
        logger.error(f"[{rid}] RAG unhandled error: {e}")
        raise

@app.get("/health")
def health():
    return {"ok": True, "docs": len(docs)}

def is_toxic(text: str) -> bool:
    return bool(TOXIC_RE.search(text or ""))

def sanitize_query(text: str) -> str:
    cleaned = INJECTION_RE.sub(" ", text or "")
    return re.sub(r"\s+", " ", cleaned).strip()

def search(text: str, top_k: int):
    if not IDX_ALL:
        raise HTTPException(503, "KB index is empty")
    vec, mat = IDX_ALL
    qv = vec.transform([text])
    sims = cosine_similarity(qv, mat).ravel()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
    return [
        {
            "source": docs[i].get("source_path") or f"idx:{i}",
            "snippet": docs[i]["text"],
            "score": float(s)
        }
        for i, s in ranked
    ]

@app.post("/rag/select")
def select(a: Req, request: Request):
    rid = getattr(request.state, "req_id", "-")

    if is_toxic(a.text):
        logger.warning(f"[{rid}] toxic query rejected")
        raise HTTPException(400, "Запрос содержит токсичную лексику и отклонён политикой использования.")

    cleaned = sanitize_query(a.text)