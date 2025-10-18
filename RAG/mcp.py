import os, sys, uuid, sqlite3
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "mosprom.hack")) if os.path.isdir("mosprom.hack") else None

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from back.logging_config import logger  # путь как в твоём проекте

DB = os.path.join(PROJECT_ROOT, "data", "runtime.sqlite")

def log_event(req_id, level, message):
    try:
        con = sqlite3.connect(DB); cur = con.cursor()
        cur.execute("INSERT INTO events(request_id, service, level, message) VALUES (?,?,?,?)",
                    (req_id, "mcp", level, message))
        con.commit(); con.close()
    except Exception as e:
        logger.error(f"[{req_id}] mcp event write error: {e}")

app = FastAPI(title="mcp-emulator")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

USERS = [
  {"user_id":"u-123","name":"Иван Петров","email":"ivan.petrov@x","dept":"buh","manager":{"id":"m-77","name":"Смирнова Е."}},
  {"user_id":"u-456","name":"Мария Орлова","email":"m.orlova@x","dept":"it","manager":{"id":"m-12","name":"Алексеев Д."}}
]

@app.middleware("http")
async def rid_mw(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.rid = rid
    resp = await call_next(request)
    return resp

@app.get("/health")
def health(): return {"ok": True, "users": len(USERS)}

class Lookup(BaseModel):
    query: str | None = None
    email: str | None = None

@app.post("/user.lookup")
def lookup(a: Lookup, request: Request):
    rid = request.state.rid
    qname = (a.query or "").strip().lower()
    qmail = (a.email or "").strip().lower()
    for u in USERS:
        if (qmail and qmail == u["email"].lower()) or (qname and qname in u["name"].lower()):
            log_event(rid, "INFO", f"user.lookup ok: {u['user_id']}")
            return {"ok": True, "user": u}
    log_event(rid, "INFO", "user.lookup not_found")
    return {"ok": False, "reason": "not_found"}

class Action(BaseModel):
    user_id: str
    reason: str

@app.post("/manager.call")
def manager_call(a: Action, request: Request):
    rid = request.state.rid
    log_event(rid, "INFO", f"manager.call -> user={a.user_id}, reason={a.reason}")
    return {"ok": True, "emulated": True, "message": f"Менеджер уведомлен: {a.reason}"}

class Ticket(BaseModel):
    user_id: str
    title: str
    body: str

@app.post("/ticket.create")
def ticket_create(t: Ticket, request: Request):
    rid = request.state.rid
    log_event(rid, "INFO", f"ticket.create -> user={t.user_id}, title={t.title[:60]}")
    return {"ok": True, "emulated": True, "ticket_id": "T-2025-0001"}