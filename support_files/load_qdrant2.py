#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import json
import uuid
import hashlib
import re
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Iterable, Optional, Union

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse

# ---------- ЛОГИРОВАНИЕ ----------
logging.basicConfig(
    filename="ingest.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------- НАСТРОЙКИ ----------

EMBEDDING_MODEL_NAME = os.path.expanduser("~/ai_models/ru-en-RoSBERTa/")

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
VECTOR_SIZE = 1024
SEPARATORS = ["\n\n", "\n", ". ", "? ", "! "]
NORMALIZE_EMBEDDINGS = True

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

COLLECTION_NAME = "roseltorg"
FILE_GLOB = "*.json"

# ---------- МОДЕЛЬ ----------
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def clean_text(text: str) -> str:
    """Очистка текста от мусора, экранированных символов, артефактов и html."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)  # убираем HTML
    text = text.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
    text = text.replace("«", "\"").replace("»", "\"")
    text = text.replace("’", "'").replace("“", "\"").replace("”", "\"")
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_chunks(long_text: str) -> List[str]:
    """Разбивает текст на перекрывающиеся чанки."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
    )
    return splitter.split_text(long_text)


PROMPT_MAP = {
    "query": "search_query",
    "passage": "search_document",
    "classification": "classification",
    "clustering": "clustering",
}


def get_embeddings_local(
    texts: Union[str, List[str]],
    mode: str = "passage",
    convert_to_numpy: bool = True,
) -> Union[List[float], List[List[float]]]:
    """Создание эмбеддингов с фоллбэком."""
    if isinstance(texts, str):
        texts_batch = [texts]
        single = True
    else:
        texts_batch = texts
        single = False

    prompt_name = PROMPT_MAP.get(mode)

    try:
        vecs = embedding_model.encode(
            texts_batch,
            prompt_name=prompt_name,
            normalize_embeddings=NORMALIZE_EMBEDDINGS,
            convert_to_numpy=convert_to_numpy,
            batch_size=64,
            show_progress_bar=False,
        )
    except TypeError:
        prefix = (prompt_name + ": ") if prompt_name else ""
        inputs = [prefix + t for t in texts_batch]
        vecs = embedding_model.encode(
            inputs,
            normalize_embeddings=NORMALIZE_EMBEDDINGS,
            convert_to_numpy=convert_to_numpy,
            batch_size=64,
            show_progress_bar=False,
        )

    if single:
        return vecs.tolist() if convert_to_numpy else vecs
    return [v.tolist() for v in vecs] if convert_to_numpy else vecs


# ---------- Qdrant ----------

def ensure_qdrant_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int = VECTOR_SIZE,
    distance: Distance = Distance.COSINE,
    recreate_on_mismatch: bool = False,
) -> None:
    assert embedding_model.get_sentence_embedding_dimension() == vector_size, \
        f"Размерность модели {embedding_model.get_sentence_embedding_dimension()} != {vector_size}"
    try:
        info = client.get_collection(collection_name)
        vp = info.config.params.vectors
        current_size = vp.size
        current_distance = vp.distance
        if current_size != vector_size or current_distance != distance:
            if recreate_on_mismatch:
                log.warning("Пересоздание коллекции %s", collection_name)
                client.recreate_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=distance),
                )
            else:
                raise ValueError(
                    f"Коллекция '{collection_name}' имеет size={current_size}, distance={current_distance}, "
                    f"ожидалось size={vector_size}, distance={distance}"
                )
    except UnexpectedResponse:
        log.info("Создаётся новая коллекция %s", collection_name)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )


def deterministic_point_id(collection: str, doc_id: str, chunk_index: int, chunk_text: str) -> str:
    name = f"{collection}|{doc_id}|{chunk_index}|" + hashlib.sha1(chunk_text.encode("utf-8")).hexdigest()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))


def iter_json_records(path: Path) -> Iterable[Dict[str, Any]]:
    """Читает JSON/JSONL."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            yield data
        elif isinstance(data, list):
            for rec in data:
                if isinstance(rec, dict):
                    yield rec
    except Exception:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if isinstance(rec, dict):
                        yield rec
                except json.JSONDecodeError:
                    continue


def is_valid_record(doc: Dict[str, Any]) -> bool:
    """Проверка на пустой или технический документ."""
    text = clean_text(doc.get("text", "")).lower()
    title = (doc.get("title") or "").strip()
    if not text or len(text) < 50:
        return False
    if text in {"текст не найден", "нет текста"}:
        return False
    if title == "Без заголовка":
        return False
    return True


def add_documents(
    client: QdrantClient,
    collection_name: str,
    docs: Iterable[Dict[str, Any]],
    text_field: str = "text",
    id_field: Optional[str] = "url",
    meta_fields: Optional[List[str]] = None,
    upsert_batch: int = 2048,
) -> int:
    ensure_qdrant_collection(client, collection_name)
    meta_fields = meta_fields or ["title", "url"]

    points: List[PointStruct] = []
    added_chunks = 0

    for doc in docs:
        if not is_valid_record(doc):
            continue

        full_text = clean_text(doc.get(text_field, ""))
        if not full_text:
            continue

        doc_id = (doc.get(id_field) or f"doc-{uuid.uuid4()}") if id_field else f"doc-{uuid.uuid4()}"
        chunks = make_chunks(full_text)
        vectors = get_embeddings_local(chunks, mode="passage")

        payload_base = {k: doc.get(k) for k in meta_fields if k in doc}
        payload_base["doc_id"] = doc_id

        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            pid = deterministic_point_id(collection_name, doc_id, i, chunk)
            payload = {
                **payload_base,
                "text": chunk,
                "chunk_index": i,
                "chunk_count": len(chunks),
            }
            points.append(PointStruct(id=pid, vector=vec, payload=payload))
            added_chunks += 1

        if len(points) >= upsert_batch:
            try:
                client.upsert(collection_name=collection_name, points=points)
            except Exception as e:
                log.error("Ошибка upsert: %s", e)
            points = []

    if points:
        try:
            client.upsert(collection_name=collection_name, points=points)
        except Exception as e:
            log.error("Ошибка upsert финального батча: %s", e)

    return added_chunks


def ingest_dir(
    data_dir: str,
    collection_name: str = COLLECTION_NAME,
    file_glob: str = FILE_GLOB,
) -> int:
    """Заливает все JSON-файлы из директории в Qdrant."""
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    total = 0

    files = sorted(Path(data_dir).glob(file_glob))
    if not files:
        log.warning("Нет файлов по шаблону %s в %s", file_glob, data_dir)
        return 0

    for path in files:
        try:
            records = list(iter_json_records(path))
            added = add_documents(
                client=client,
                collection_name=collection_name,
                docs=records,
                text_field="text",
                id_field="url",
                meta_fields=["title", "url"],
            )
            log.info("%s: добавлено чанков %d", path.name, added)
            total += added
        except Exception as e:
            log.error("Ошибка при обработке %s: %s", path, e)

    log.info("Готово. Всего добавлено чанков: %d", total)
    return total


# ---------- CLI ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка JSON-файлов в Qdrant")
    parser.add_argument("data_dir", help="Путь к директории с JSON файлами")
    parser.add_argument("--collection", default=COLLECTION_NAME, help="Имя коллекции Qdrant")
    parser.add_argument("--glob", default=FILE_GLOB, help="Маска файлов, по умолчанию *.json")
    args = parser.parse_args()

    ingest_dir(args.data_dir, collection_name=args.collection, file_glob=args.glob)
