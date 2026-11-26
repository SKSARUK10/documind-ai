from langchain_core.embeddings import Embeddings

from app.services import vector_store_service
from app.services.vector_store_service import (
    create_vector_store,
    search_vector_store,
)


class FakeEmbeddingModel(Embeddings):
    """Deterministic embeddings: no API key and no network call."""

    def _embed(self, text: str) -> list[float]:
        normalized = text.lower()

        return [
            1.0 if "python" in normalized else 0.0,
            1.0 if "fastapi" in normalized else 0.0,
        ]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


def use_fake_embeddings(monkeypatch) -> None:
    monkeypatch.setattr(
        vector_store_service,
        "create_embedding_model",
        lambda: FakeEmbeddingModel(),
    )


def test_create_vector_store(monkeypatch) -> None:
    use_fake_embeddings(monkeypatch)

    chunks = [
        {
            "page_number": 1,
            "text": "Python is a programming language.",
        },
        {
            "page_number": 2,
            "text": "FastAPI is a Python web framework.",
        },
    ]

    vector_store = create_vector_store(chunks, "doc-1")

    assert vector_store is not None
    assert len(vector_store.docstore._dict) == 2


def test_search_vector_store(monkeypatch) -> None:
    use_fake_embeddings(monkeypatch)

    chunks = [
        {
            "page_number": 1,
            "text": "Python is a programming language.",
        },
        {
            "page_number": 2,
            "text": "FastAPI is a Python web framework.",
        },
    ]

    vector_store = create_vector_store(chunks, "doc-1")

    results = search_vector_store(
        vector_store,
        "What is Python?",
        k=1,
    )

    assert len(results) == 1
    assert results[0]["text"] == "Python is a programming language."
    assert results[0]["document_id"] == "doc-1"
    assert results[0]["page_number"] == 1
