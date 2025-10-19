import os
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from normalize_query import normalise_query, TERMINS
import warnings

# Подавляем предупреждения о неинициализированных весах
warnings.filterwarnings("ignore", message="Some weights of.*were not initialized")

# ✅ Определяем устройство
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"✅ Используется устройство: {device}")
if device.type == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# ✅ Правильный путь к локальной модели (без 'root/' в начале)
model_path = "/root/ai_models/ru-en-RoSBERTa"

# ✅ Загружаем токенизатор и модель с указанием локального пути
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModel.from_pretrained(model_path, local_files_only=True)

# ✅ Переводим модель на GPU, включаем half precision и eval
if device.type == "cuda":
    model = model.to(device).half()
else:
    model = model.to(device)
model.eval()

# 🔹 Функция получения эмбеддингов
def get_embeddings(texts, remove_prefix=True):
    processed_texts = []
    for text in texts:
        if remove_prefix and text.startswith("search_query:"):
            text = text[len("search_query:"):].strip()
        processed_texts.append(text)

    inputs = tokenizer(
        processed_texts,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]  # [CLS] токен
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

    return embeddings.cpu().numpy()

# 🔹 Обработка списка запросов
def process_queries(queries, termins=TERMINS, batch_size=8):
    results = []
    normalized_queries = [normalise_query(q, termins) for q in queries]

    for i in range(0, len(normalized_queries), batch_size):
        batch = normalized_queries[i:i+batch_size]
        batch_embeddings = get_embeddings(batch)

        for query, norm_q, emb in zip(queries[i:i+batch_size], batch, batch_embeddings):
            results.append({
                "original_query": query,
                "normalized_query": norm_q,
                "embedding": emb,
                "embedding_shape": emb.shape,
                "embedding_norm": np.linalg.norm(emb)
            })
    return results

# 🔹 Пример использования
if __name__ == "__main__":
    test_queries = [
        "Как оформить ЭДО для 44 фз и использовать ЛК оператора?",
        "Какие требования к электронной подписи по 223-ФЗ?"
    ]

    results = process_queries(test_queries)

    for i, result in enumerate(results):
        print(f"\n--- Запрос {i+1} ---")
        print(f"Оригинал: {result['original_query']}")
        print(f"Нормализованный: {result['normalized_query']}")
        print(f"Размерность эмбеддинга: {result['embedding_shape']}")
        print(f"Норма эмбеддинга: {result['embedding_norm']:.4f}")

    # 🔹 Сравнение схожести
    from sklearn.metrics.pairwise import cosine_similarity

    print("\n--- Сравнение эмбеддингов ---")
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            sim = cosine_similarity(
                [results[i]['embedding']],
                [results[j]['embedding']]
            )[0][0]
            print(f"Схожесть запроса {i+1} и {j+1}: {sim:.4f}")
