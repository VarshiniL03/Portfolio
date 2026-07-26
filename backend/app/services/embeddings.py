"""
Embedding generation via Cohere's hosted API — deliberately NOT using a
local model (sentence-transformers/torch) here, since that combination is
too memory-heavy for free-tier hosting (Render's 512MB limit). Cohere's
embed-english-light-v3.0 model outputs 384-dim vectors, matching our
existing database schema exactly.
"""
import cohere

from app.core.config import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = cohere.Client(settings.COHERE_API_KEY)
    return _client


def get_embedding(text: str) -> list[float]:
    client = _get_client()
    response = client.embed(
        texts=[text.replace("\n", " ").strip()],
        model="embed-english-light-v3.0",
        input_type="search_document",
    )
    return response.embeddings[0]


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    client = _get_client()
    cleaned = [t.replace("\n", " ").strip() for t in texts]
    response = client.embed(
        texts=cleaned,
        model="embed-english-light-v3.0",
        input_type="search_document",
    )
    return response.embeddings