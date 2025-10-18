# system.py  (или rag_tfidf/api.py)
import os, json, uuid, re
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os, sys

# абсолютный путь до "mosprom.hack"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from back.logging_config import logger

#безопасность и константы
MIN_THRESHOLD = 0.70        # не позволяем занижать
DEFAULT_THRESHOLD = float(os.getenv("THRESHOLD", "0.75"))
DEFAULT_THRESHOLD = max(DEFAULT_THRESHOLD, MIN_THRESHOLD)

TOP_K_DEFAULT = int(os.getenv("TOP_K", "5"))
MAX_TOP_K = 10

# простой фильтр токсичности
TOXIC_PATTERNS = [
    r"\b(идиот|дурак|туп(ой|ица)|сука|бл(я|)(т|д)|мразь|ненавижу|убью)\b",
    r"расстрел|угрожаю|повеш",           # угрозы
]
TOXIC_RE = re.compile("|".join(TOXIC_PATTERNS), re.IGNORECASE)

# базовая защита от prompt-injection (на стороне поиска)
INJECTION_RE = re.compile(
    r"(игнорируй предыдущее|ignore previous|системный промпт|system prompt|"
    r"выполни команду|execute|curl|http://|https://)",
    re.IGNORECASE
)

# Данные (моки)
docs = []
with open("data/ingest.ndjson", encoding="utf-8") as f:
    for line in f:
        try:
            d = json.loads(line)
            if (d.get("text") or "").strip():
                docs.append(d)
        except Exception as e:
            logger.error(f"Не удалось прочитать строку NDJSON: {e}")

if not docs:
    logger.error("Пустая база знаний: data/kb/ingest.ndjson не содержит документов")
    # не падаем, но любые запросы вернут 503

# индексы
def build_index(items):
    texts = [it["text"] for it in items]
    vec = TfidfVectorizer(analyzer="word", ngram_range=(1,2), min_df=1).fit(texts)
    mat = vec.transform(texts)
    return vec, mat

IDX_ALL = build_index(docs) if docs else None
IDX_BY = {}
for dom in ("it", "hr", "buh"):
    sub = [d for d in docs if d.get("domain") == dom]
    if sub:
        IDX_BY[dom] = (sub, *build_index(sub))

app = FastAPI(title="rag-select-tfidf (secure)")

class Req(BaseModel):
    text: str
    domain: Optional[str] = None
    top_k: int = TOP_K_DEFAULT
    threshold: float = DEFAULT_THRESHOLD

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # request_id в контекст логов
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.req_id = req_id
    logger.info(f"[{req_id}] RAG request -> {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"[{req_id}] RAG response <- {request.url.path} {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"[{req_id}] Неперехваченная ошибка RAG: {e}")
        raise

@app.get("/health")
def health():
    return {"ok": True, "docs": len(docs), "domains": list(IDX_BY.keys())}

def is_toxic(text: str) -> bool:
    return bool(TOXIC_RE.search(text or ""))

def sanitize_query(text: str) -> str:
    # вырезаем инъекции и внешние ссылки
    cleaned = INJECTION_RE.sub(" ", text or "")
    return re.sub(r"\s+", " ", cleaned).strip()

def search(text: str, domain: Optional[str], top_k: int):
    if not IDX_ALL:
        raise HTTPException(503, "KB index is empty")
    # доменный поиск, если индекс есть
    if domain and domain in IDX_BY:
        sub, vec, mat = IDX_BY[domain]
        qv = vec.transform([text])
        sims = cosine_similarity(qv, mat).ravel()
        ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            {"source": sub[i]["source_path"], "snippet": sub[i]["text"], "score": float(s),
             "domain": sub[i].get("domain")}
            for i, s in ranked
        ]
    # общий индекс
    vec, mat = IDX_ALL
    qv = vec.transform([text])
    sims = cosine_similarity(qv, mat).ravel()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
    return [
        {"source": docs[i]["source_path"], "snippet": docs[i]["text"], "score": float(s),
         "domain": docs[i].get("domain")}
        for i, s in ranked
    ]


@app.post("/rag/select")
def select(a: Req, request: Request):
    req_id = getattr(request.state, "req_id", "-")
    # этика/безопасность
    if is_toxic(a.text):
        logger.warning(f"[{req_id}] Токсичный запрос отклонён")
        raise HTTPException(400, "Запрос содержит токсичную лексику и отклонён политикой использования.")
    # запрет внешних исходящих запросов
    # RAG вообще не делает HTTP-вызовов — дополнительно отсекаем попытки протолкнуть URL/command
    cleaned = sanitize_query(a.text)
    if not cleaned:
        logger.warning(f"[{req_id}] Пустой запрос после санации")
        raise HTTPException(400, "Запрос пуст после очистки от потенциально опасного содержимого.")

    # пороги/валидация параметров
    top_k = min(max(1, a.top_k), MAX_TOP_K)
    threshold = max(a.threshold, MIN_THRESHOLD)  # не даём опустить ниже MIN_THRESHOLD

    # поиск
    try:
        cands = search(cleaned, domain=a.domain, top_k=top_k)
    except HTTPException:
        logger.error(f"[{req_id}] KB пустая — вернули 503")
        raise
    except Exception as e:
        logger.error(f"[{req_id}] Ошибка поиска: {e}")
        raise HTTPException(500, "Внутренняя ошибка поиска")

    eligible = [c for c in cands if c["score"] >= threshold]
    max_score = max([c["score"] for c in cands], default=0.0)
    coverage = round(len(eligible) / top_k, 2)
    passed = bool(max_score >= threshold)

    # логирование результата
    logger.info(
        f"[{req_id}] RAG: domain={a.domain} top_k={top_k} thr={threshold} "
        f"max={round(max_score, 3)} covered={coverage} passed={passed}"
    )

    return {
        "query": cleaned,
        "domain": a.domain,
        "top_k": top_k,
        "threshold": threshold,
        "candidates": cands,
        "eligible_contexts": eligible,
        "max_score": round(max_score, 3),
        "coverage": coverage,
        "passed": passed,
        "note": "tfidf mock (secure)"
    }