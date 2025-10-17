from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="mcp-emulator")

#если фронт будет звать напрямую из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

#мок-данные пользователей
USERS = [
  {"user_id":"u-123","name":"Иван Петров","email":"ivan.petrov@x","dept":"buh","manager":{"id":"m-77","name":"Смирнова Е."}},
  {"user_id":"u-456","name":"Мария Орлова","email":"m.orlova@x","dept":"it","manager":{"id":"m-12","name":"Алексеев Д."}}
]

#healthcheck
@app.get("/health")
def health():
    return {"ok": True, "users": len(USERS)}

#модели запросов
class Lookup(BaseModel):
    query: str | None = None
    email: str | None = None

@app.post("/user.lookup")
def lookup(a: Lookup):
    qname = (a.query or "").strip().lower()
    qmail = (a.email or "").strip().lower()
    for u in USERS:
        if (qmail and qmail == u["email"].lower()) or (qname and qname in u["name"].lower()):
            return {"ok": True, "user": u}
    return {"ok": False, "reason": "not_found"}

class Action(BaseModel):
    user_id: str
    reason: str

@app.post("/manager.call")
def manager_call(a: Action):
    return {"ok": True, "emulated": True, "message": f"Менеджер уведомлен: {a.reason}"}

class Ticket(BaseModel):
    user_id: str
    title: str
    body: str

@app.post("/ticket.create")
def ticket_create(t: Ticket):
    return {"ok": True, "emulated": True, "ticket_id": "T-2025-0001"}