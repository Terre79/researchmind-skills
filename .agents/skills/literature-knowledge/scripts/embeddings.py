"""Token-service configuration and real embedding requests."""
import math
import os

from http_client import request


def configuration():
    if google_key := os.getenv("GOOGLE_API_KEY"):
        return "google", os.getenv("GOOGLE_EMBEDDING_MODEL", "gemini-embedding-001"), google_key, ""
    model = os.getenv("OPENAI_EMBEDDING_MODEL")
    key = os.getenv("OPENAI_API_KEY")
    if not model or not key:
        raise RuntimeError("Set GOOGLE_API_KEY or both OPENAI_API_KEY and OPENAI_EMBEDDING_MODEL")
    return "openai", model, key, os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")


def embedded(config, texts):
    provider, model, key, base = config
    if provider == "google":
        url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":batchEmbedContents"
        body = {"requests": [{"model": "models/" + model, "content": {"parts": [{"text": text}]}}
                              for text in texts]}
        data = request(url, body, {"x-goog-api-key": key}, timeout=120)
        vectors = [row["values"] for row in data["embeddings"]]
    else:
        data = request(base + "/embeddings", {"model": model, "input": texts},
                       {"Authorization": f"Bearer {key}"}, timeout=120)
        vectors = [row["embedding"] for row in sorted(data["data"], key=lambda row: row["index"])]
    if len(vectors) != len(texts) or not all(vector and all(math.isfinite(x) for x in vector)
                                             for vector in vectors):
        raise ValueError("Embedding service returned invalid vectors")
    return vectors
