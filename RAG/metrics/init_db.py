import sqlite3, pathlib, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "runtime.sqlite"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

con = sqlite3.connect(DB_PATH.as_posix()); cur = con.cursor()

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

con.commit(); con.close()
print(f"db ok -> {DB_PATH}")