import os, sys, uuid, json, sqlite3
from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from back.logging_config import logger

DB = os.path.join(PROJECT_ROOT, "data", "runtime.sqlite")
RAG_URL = os.getenv("RAG_URL", "http://127.0.0.1:8008/rag/select")
MCP_URL = os.getenv("MCP_URL", "http://127.0.0.1:8006")
THRESHOLD = float(os.getenv("THRESHOLD", "0.75"))
TOP_K = int(os.getenv("TOP_K", "5"))

def log_event(req_id, level, message):
    try:
        con = sqlite3.connect(DB); cur = con.cursor()
        cur.execute("INSERT INTO events(request_id, service, level, message) VALUES (?,?,?,?)",
                    (req_id, "gateway", level, message))
        con.commit(); con.close()
    except Exception as e:
        logger.error(f"[{req_id}] gateway event write error: {e}")

def log_interaction(row: dict):
    con = sqlite3.connect(DB); cur = con.cursor()
    cur.execute("""
        INSERT INTO interactions(user_id, query, pred_class, pred_conf, escalate, sources_json)
        VALUES (?,?,?,?,?,?)
    """, (
        row.get("user_id"), row["query"], row.get("pred_class"),
        row.get("pred_conf", 0.0), 1 if row["escalate"] else 0,
        json.dumps(row.get("sources", []), ensure_ascii=False)
    ))
    con.commit(); con.close()

def safe_post(client, url, payload):
    try:
        r = client.post(url, json=payload)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

app = FastAPI(title="gateway")

class Ask(BaseModel):
    text: str
    email: str | None = None

@app.get("/health")
def health(): return {"ok": True, "rag": RAG_URL, "mcp": MCP_URL}

@app.post("/answer")
def answer(a: Ask, request: Request):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    with httpx.Client(timeout=15.0, headers={"X-Request-ID": rid}) as C:
        # MCP lookup
        lookup, err_lookup = safe_post(C, f"{MCP_URL}/user.lookup", {"email": a.email, "query": None})
        user = lookup.get("user") if (lookup and lookup.get("ok")) else None
        if user: log_event(rid, "INFO", f"user {user['user_id']} lookup ok")
        else:    log_event(rid, "INFO", "user lookup miss")

        # RAG select
        sel, err_rag = safe_post(C, RAG_URL, {"text": a.text, "top_k": TOP_K, "threshold": THRESHOLD})

        # безопасный парсинг
        contexts, sources, max_score, passed = [], [], 0.0, False
        if err_rag or not isinstance(sel, dict):
            log_event(rid, "ERROR", f"rag/select failed: {err_rag or 'no json'}")
        else:
            try:
                ctx = sel.get("eligible_contexts") or sel.get("candidates") or []
                for c in ctx:
                    if isinstance(c, dict):
                        src = c.get("source") or c.get("url") or "unknown"
                        snip = c.get("snippet") or ""
                        sc = float(c.get("score") or 0.0)
                        contexts.append({"source": src, "snippet": snip, "score": sc})
                        sources.append(src)
                max_score = float(sel.get("max_score", 0.0))
                passed = bool(sel.get("passed", False))
            except Exception as e:
                log_event(rid, "ERROR", f"rag/select parse error: {e}")
                contexts, sources, max_score, passed = [], [], 0.0, False

        escalate = not passed
        if escalate:
            log_event(rid, "INFO", "escalation=1 (low confidence)")
            if user:
                safe_post(C, f"{MCP_URL}/manager.call",
                          {"user_id": user["user_id"], "reason": "Низкая уверенность RAG"})
                safe_post(C, f"{MCP_URL}/ticket.create",
                          {"user_id": user["user_id"], "title": a.text, "body": "Авто-сводка контекста"})
                log_event(rid, "INFO", f"message forwarded to manager of {user['user_id']}")

    log_interaction({
        "user_id": user["user_id"] if user else None,
        "query": a.text,
        "pred_class": None,
        "pred_conf": 0.0,
        "escalate": escalate,
        "sources": sources
    })

    summary = " ".join([c.get("snippet","") for c in contexts[:2]]) or "Недостаточно данных."
    return {
        "eligible_contexts": contexts,
        "max_score": max_score,
        "threshold": THRESHOLD,
        "passed": passed,
        "answer": summary,
        "escalate": escalate,
        "user": user
    }