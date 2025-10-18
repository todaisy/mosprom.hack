import os, sys, sqlite3
from fastapi import FastAPI, Query

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB = os.path.join(PROJECT_ROOT, "data", "runtime.sqlite")

app = FastAPI(title="metrics")

def q(sql, args=()):
    con = sqlite3.connect(DB); cur = con.cursor()
    rows = cur.execute(sql, args).fetchall()
    con.close()
    return rows

@app.get("/health")
def health():
    try:
        total = q("select count(*) from interactions")[0][0]
        return {"ok": True, "interactions": total}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/stats/summary")
def summary():
    total = q("select count(*) from interactions")[0][0]
    esc = q("select count(*) from interactions where escalate=1")[0][0]
    return {"total": total, "escalations": esc}

@app.get("/events")
def events(limit: int = Query(100, ge=1, le=1000)):
    rows = q("""
      select ts, request_id, service, level, message
      from events order by ts desc limit ?
    """, (limit,))
    return {"rows": [
        {"ts": ts, "request_id": rid, "service": svc, "level": lvl, "message": msg}
        for ts, rid, svc, lvl, msg in rows
    ]}