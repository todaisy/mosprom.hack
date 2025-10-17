import os, json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TOP_K = int(os.getenv("TOP_K", "5"))
THR = float(os.getenv("THRESHOLD", "0.75"))

# грузим мок-доки
docs = []
with open("data/ingest.ndjson", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        docs.append(d)

# готовим TF-IDF отдельно по доменам и общий
def build_index(items):
    texts = [it["text"] for it in items]
    vec = TfidfVectorizer(analyzer="word", ngram_range=(1,2), min_df=1).fit(texts)
    mat = vec.transform(texts)
    return vec, mat

IDX_ALL = build_index(docs)
IDX_BY = {
    dom: build_index([d for d in docs if d.get("domain")==dom])
    for dom in {"it","hr","buh"}
}

def search(text, domain=None, top_k=TOP_K):
    if domain in IDX_BY and len([d for d in docs if d.get("domain")==domain])>0:
        sub = [d for d in docs if d.get("domain")==domain]
        vec, mat = IDX_BY[domain]
        qv = vec.transform([text])
        sims = cosine_similarity(qv, mat).ravel()
        ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
        items = []
        for i, s in ranked:
            d = sub[i]
            items.append({"source": d["source_path"], "snippet": d["text"], "score": float(s), "domain": d.get("domain")})
        return items
    # общий индекс
    vec, mat = IDX_ALL
    qv = vec.transform([text])
    sims = cosine_similarity(qv, mat).ravel()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
    items = []
    for i, s in ranked:
        d = docs[i]
        items.append({"source": d["source_path"], "snippet": d["text"], "score": float(s), "domain": d.get("domain")})
    return items

app = FastAPI(title="rag-select-tfidf")

class Req(BaseModel):
    text: str
    domain: Optional[str] = None
    top_k: int = TOP_K
    threshold: float = THR

@app.post("/rag/select")
def select(a: Req):
    cands = search(a.text, domain=a.domain, top_k=a.top_k)
    eligible = [c for c in cands if c["score"] >= a.threshold]
    max_score = max([c["score"] for c in cands], default=0.0)
    coverage = round(len(eligible)/max(1, a.top_k), 2)
    return {
        "query": a.text,
        "domain": a.domain,
        "top_k": a.top_k,
        "threshold": a.threshold,
        "candidates": cands,
        "eligible_contexts": eligible,
        "max_score": round(max_score,3),
        "coverage": coverage,
        "passed": bool(max_score >= a.threshold),
        "note": f"tfidf mock; top_k={a.top_k}, threshold={a.threshold}"
    }