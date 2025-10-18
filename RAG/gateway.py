# gateway.py
# -*- coding: utf-8 -*-

import os, sys, uuid, json, sqlite3
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------- пути, чтобы видеть back/ и orchestrator ----------
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# если структура вида mosprom/mosprom.hack/{back,RAG,...}
HACK = os.path.join(ROOT, "mosprom.hack")
if os.path.isdir(HACK) and HACK not in sys.path:
    sys.path.insert(0, HACK)

# логгер
try:
    from back.logging_config import logger
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("gateway")

# оркестратор (наша единая функция)
from orchestrator import rag_answer  # ensure orchestrator.py лежит рядом с этим файлом

# ---------- конфиг ----------
DB = os.path.join(ROOT, "mosprom.hack", "data", "runtime.sqlite")  # правь путь при необходимости
os.makedirs(os.path.dirname(DB), exist_ok=True)

# ---------- утилиты записи метрик ----------
def log_event(req_id: str, level: str, message: str) -> None:
    try:
        con = sqlite3.connect(DB); cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                request_id TEXT,
                service TEXT,
                level TEXT,
                message TEXT
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_events_req ON events(request_id);")
        cur.execute(
            "INSERT INTO events(request_id, service, level, message) VALUES (?,?,?,?)",
            (req_id, "gateway", level, message)
        )
        con.commit(); con.close()
    except Exception as e:
        logger.error(f"[{req_id}] gateway event write error: {e}")

def log_interaction(row: Dict[str, Any]) -> None:
    try:
        con = sqlite3.connect(DB); cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS interactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                query TEXT,
                pred_class TEXT,
                pred_conf REAL,
                escalate INTEGER,
                sources_json TEXT
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_ts ON interactions(ts);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_class ON interactions(pred_class);")

        cur.execute("""
            INSERT INTO interactions(user_id, query, pred_class, pred_conf, escalate, sources_json)
            VALUES (?,?,?,?,?,?)
        """, (
            row.get("user_id"),
            row.get("query"),
            row.get("pred_class"),
            float(row.get("pred_conf") or 0.0),
            1 if row.get("escalate") else 0,
            json.dumps(row.get("sources", []), ensure_ascii=False)
        ))
        con.commit(); con.close()
    except Exception as e:
        logger.error(f"[{row.get('request_id','?')}] gateway interactions write error: {e}")

# ---------- FastAPI ----------
app = FastAPI(title="gateway")

# CORS (если нужен фронт из браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

class Ask(BaseModel):
    text: str
    email: Optional[str] = None

@app.get("/health")
def health():
    try:
        total = 0
        con = sqlite3.connect(DB); cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS interactions(id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, user_id TEXT, query TEXT, pred_class TEXT, pred_conf REAL, escalate INTEGER, sources_json TEXT);")
        cur.execute("SELECT count(*) FROM interactions")
        total = cur.fetchone()[0]
        con.close()
        return {"ok": True, "db": DB, "interactions": total}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/answer")
def answer(a: Ask, request: Request):
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    try:
        # 1) оркестратор делает: класс → эмбеддинг → Qdrant → (эскалация MCP?) → Qwen
        out = rag_answer(a.text, a.email)

        # 2) лог событий
        msg = "escalate" if out.get("escalate") else "ok"
        log_event(req_id, "INFO", f"/answer {msg}; max_score={out.get('max_score')}")

        # 3) лог взаимодействия (для дашборда)
        user = out.get("user") or {}
        sources = [c.get("source") for c in out.get("eligible_contexts", []) if isinstance(c, dict)]
        log_interaction({
            "request_id": req_id,
            "user_id": user.get("user_id"),
            "query": a.text,
            "pred_class": out.get("pred_class"),
            "pred_conf": out.get("pred_conf", 0.0),
            "escalate": out.get("escalate", False),
            "sources": sources
        })

        # 4) единый ответ фронту (готовая строка пользователю в поле final_text)
        return {
            "request_id": req_id,
            **out  # включает: final_text, passed, escalate, user, eligible_contexts, max_score, pred_class, pred_conf
        }

    except Exception as e:
        logger.error(f"[{req_id}] /answer error: {e}")
        log_event(req_id, "ERROR", f"/answer failed: {e}")
        return {
            "request_id": req_id,
            "final_text": "Произошла внутренняя ошибка. Мы уже разбираемся.",
            "passed": False,
            "escalate": True
        }