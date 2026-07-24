"""
Local embedding generation using sentence-transformers — no API key, no
cost, runs entirely on your machine. Model downloads once (~90MB) on first use.
"""
from sentence_transformers import SentenceTransformer

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dimensional embeddings
    return _model


def get_embedding(text: str) -> list[float]:
    model = _get_model()
    return model.encode(text.replace("\n", " ").strip()).tolist()


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    model = _get_model()
    cleaned = [t.replace("\n", " ").strip() for t in texts]
    return model.encode(cleaned).tolist()