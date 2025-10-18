import os, requests

BASE  = os.getenv("QWEN_OLLAMA_BASE", "http://localhost:11434")
MODEL = os.getenv("QWEN_OLLAMA_MODEL", "qwen3:4b")
TEMP  = float(os.getenv("QWEN_TEMP", "0.2"))
MAX_TOKENS = int(os.getenv("QWEN_MAX_TOKENS", "1024"))

def qwen_generate(messages, max_tokens=None, temperature=None) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": TEMP if temperature is None else float(temperature),
            "num_predict": MAX_TOKENS if max_tokens is None else int(max_tokens),
        },
    }
    r = requests.post(f"{BASE}/api/chat", json=payload, timeout=180)
    r.raise_for_status()
    js = r.json()
    return ((js.get("message") or {}).get("content") or "").strip()