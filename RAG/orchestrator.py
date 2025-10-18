# -*- coding: utf-8 -*-
"""
Единая функция rag_answer(...) + опциональный FastAPI-эндпоинт /assist.
Зависимости: requests, qdrant-client, support_files.load_qdrant.get_embeddings_local,
Qwen клиент (OpenAI-совместимый) через llm_qwen_openai.py
"""

import os, sys, re, json, uuid
from typing import List, Dict, Tuple, Optional

# ---- пути (чтобы видеть back/ и support_files/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# ---- логгер
try:
    from back.logging_config import logger
except Exception:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("orchestrator")

#Qdrant + эмбеддинги (RoSBERTa)
from qdrant_client import QdrantClient
from support_files.load_qdrant import get_embeddings_local, QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME

# ---- MCP (эмулятор)
import requests

MCP_URL = os.getenv("MCP_URL", "http://127.0.0.1:8006")

# ---- Порог/поиск
TOP_K = int(os.getenv("TOP_K", "5"))
THRESHOLD = float(os.getenv("THRESHOLD", "0.75"))
MIN_THRESHOLD = 0.70
THRESHOLD = max(THRESHOLD, MIN_THRESHOLD)

import os
if os.getenv("QWEN_PROVIDER", "").lower() == "ollama":
    from qwen import qwen_generate
else:
    from qwen import qwen_generate

# лёгкая детерминированная классификация (fallback; финально дублируем в промпте)
IT_PAT = re.compile(
    r"\b(vpn|wi[- ]?fi|wifi|драйвер|принтер|почт|почта|аккаунт|парол|локаль|windows|ошибка|сбой|vpn\s*809)\b", re.I)
HR_PAT = re.compile(r"\b(отпуск|больничн|командировк|кадр|кадры|трудов|договор|оформлен|прием|увольнен)\b", re.I)
BUH_PAT = re.compile(r"\b(счет|счёт|акта?|накладн|оплат|бух|проводк|1c|1с|дебет|кредит|смет|налог|сверк)\b", re.I)

ESCALATE_PAT = re.compile(r"\b(позвоните|свяжитесь|оператор|менеджер|начальник|живой человек|жалоб|эскалац)\b", re.I)


def classify_text(text: str) -> Tuple[str, float, bool]:
    t = text or ""
    scores = {
        "IT": 1.0 if IT_PAT.search(t) else 0.0,
        "HR": 1.0 if HR_PAT.search(t) else 0.0,
        "BUH": 1.0 if BUH_PAT.search(t) else 0.0
    }
    label = max(scores, key=scores.get)
    conf = scores[label]
    escalate_hint = bool(ESCALATE_PAT.search(t))
    # если ничего не совпало, ставим низкую уверенность и класс IT по умолчанию
    if conf == 0.0:
        label, conf = "IT", 0.33
    return label, conf, escalate_hint


# поиск в Qdrant
QDR = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
COLL = os.getenv("QDRANT_COLLECTION", COLLECTION_NAME)


def qdrant_search(text: str, top_k: int = TOP_K, threshold: float = THRESHOLD) -> Tuple[List[Dict], float, bool]:
    qvec = get_embeddings_local(text, mode="query")
    try:
        res = QDR.search(
            collection_name=COLL,
            query_vector=qvec,
            limit=top_k,
            score_threshold=threshold,
            with_payload=True,
            with_vectors=False,
        )
        items = [{
            "source": r.payload.get("url") or r.payload.get("doc_id") or str(r.id),
            "snippet": r.payload.get("text", ""),
            "score": float(r.score)
        } for r in res]
        if not items:
            res2 = QDR.search(collection_name=COLL, query_vector=qvec, limit=top_k, with_payload=True)
            items = [{
                "source": r.payload.get("url") or r.payload.get("doc_id") or str(r.id),
                "snippet": r.payload.get("text", ""),
                "score": float(r.score)} for r in res2]
        max_score = max([c["score"] for c in items], default=0.0)
        passed = bool(max_score >= threshold)
        return items, max_score, passed
    except Exception as e:
        logger.error(f"qdrant_search error: {e}")
        return [], 0.0, False


# MCP: lookup + эскалация
def mcp_lookup(email: Optional[str]) -> Optional[Dict]:
    if not email:
        return None
    try:
        r = requests.post(f"{MCP_URL}/user.lookup", json={"email": email, "query": None}, timeout=5)
        if r.ok and r.json().get("ok"):
            return r.json().get("user")
    except Exception as e:
        logger.error(f"mcp_lookup error: {e}")
    return None


def mcp_escalate(user: Optional[Dict], reason: str, title: str, body: str) -> None:
    try:
        if user:
            requests.post(f"{MCP_URL}/manager.call",
                          json={"user_id": user["user_id"], "reason": reason}, timeout=5)
            requests.post(f"{MCP_URL}/ticket.create",
                          json={"user_id": user["user_id"], "title": title, "body": body}, timeout=5)
        else:
            # нет пользователя — всё равно создадим тикет с пустым user_id
            requests.post(f"{MCP_URL}/ticket.create",
                          json={"user_id": "unknown", "title": title, "body": body}, timeout=5)
    except Exception as e:
        logger.error(f"mcp_escalate error: {e}")

# Qwen: сборка сообщений и генерация итогового ответа
def build_qwen_messages(query: str, contexts: List[Dict], coarse_label: str) -> list:
    ctx_str = ""
    for i, c in enumerate(contexts[:5], 1):
        ctx_str += f"[{i}] score={round(float(c.get('score', 0.0)), 3)} src={c.get('source', 'unknown')}\n{(c.get('snippet') or '').replace('\n', ' ')}\n\n"
    system = (
        "Ты корпоративный ассистент службы поддержки. "
        "Отвечай строго по приведённым материалам. Если фактов недостаточно — так и скажи, предложи передать оператору. "
        "Никаких внешних запросов и домыслов."
    )
    user = (
        f"Запрос: {query}\n"
        f"Грубая классификация (эвристика): {coarse_label}\n\n"
        f"Материалы:\n{ctx_str}\n"
        "Инструкции:\n"
        "- Дай краткий и точный ответ на русском.\n"
        "- Если контекста не хватает — напиши 'Недостаточно данных'.\n"
        "- Классифицируй как один из: IT | HR | BUH.\n"
        "- Верни ТОЛЬКО JSON:\n"
        "{\n"
        "  \"answer\": \"<текст>\",\n"
        "  \"class\": \"IT|HR|BUH\",\n"
        "  \"confidence\": <0..1>,\n"
        "  \"sources\": [индексы использованных фрагментов, начиная с 1]\n"
        "}\n"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]


def run_qwen(query: str, contexts: List[Dict], coarse_label: str) -> Tuple[str, Optional[str], float]:
    if not contexts:
        return "Недостаточно данных.", None, 0.0
    msgs = build_qwen_messages(query, contexts, coarse_label)
    raw = qwen_generate(msgs, max_tokens=400, temperature=0.1)
    # пытаемся выдрать JSON
    try:
        j = json.loads(raw)
    except Exception:
        start, end = raw.find("{"), raw.rfind("}")
        j = json.loads(raw[start:end + 1]) if (start != -1 and end != -1 and end > start) else {}

    answer = (j.get("answer") or "").strip() if isinstance(j, dict) else ""
    label = (j.get("class") or "").strip().upper() if isinstance(j, dict) else None
    conf = float(j.get("confidence") or 0.0) if isinstance(j, dict) else 0.0
    if not answer:
        answer = "Недостаточно данных."
    return answer, (label if label in {"IT", "HR", "BUH"} else None), conf


#Главная функция
def rag_answer(text: str, email: Optional[str] = None) -> Dict:
    req_id = str(uuid.uuid4())
    text = (text or "").strip()
    if not text:
        return {"final_text": "Введите текст запроса.", "escalate": False, "passed": False}

    # грубая классификация + подсказка на эскалацию
    label, label_conf, escalate_hint = classify_text(text)

    # Qdrant retrieve
    contexts, max_score, passed = qdrant_search(text, TOP_K, THRESHOLD)

    # решаем об эскалации: низкая уверенность RAG ИЛИ явная просьба к человеку
    should_escalate = (not passed) or escalate_hint

    # MCP: lookup
    user = mcp_lookup(email)

    if should_escalate:
        # вызвать менеджера + создать тикет
        reason = "Низкая уверенность RAG" if not passed else "Пользователь просит оператора"
        mcp_escalate(user, reason=reason, title=text, body="Автоэскалация из ассистента")
        return {
            "final_text": "Не удалось найти в базе знаний подходящего ответа, передали ваш вопрос менеджеру.",
            "passed": passed,
            "escalate": True,
            "user": user,
            "eligible_contexts": contexts,
            "max_score": max_score,
            "pred_class": label,
            "pred_conf": label_conf
        }

    #Генерация Qwen на основе контекстов
    answer_text, llm_class, llm_conf = run_qwen(text, contexts, label)

    return {
        "final_text": answer_text,
        "passed": passed,
        "escalate": False,
        "user": user,
        "eligible_contexts": contexts,
        "max_score": max_score,
        "pred_class": llm_class or label,
        "pred_conf": llm_conf if llm_class else label_conf
    }


# (опционально) HTTP-обёртка для быстрого вызова:
#   uvicorn orchestrator:app --port 8011 --reload
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="orchestrator")


class Ask(BaseModel):
    text: str
    email: Optional[str] = None


@app.post("/assist")
def assist(a: Ask):
    return rag_answer(a.text, a.email)
