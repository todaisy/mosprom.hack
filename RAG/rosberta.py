from sentence_transformers import SentenceTransformer
m = SentenceTransformer("ai-forever/ru-en-RoSBERTa")
m.save("models/ru-en-RoSBERTa")  # сохранит папку с весами локально
print("OK:", m.get_sentence_embedding_dimension(), "dims")