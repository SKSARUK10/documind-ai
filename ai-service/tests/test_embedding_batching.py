from types import SimpleNamespace

from app.services.embedding_service import (
    EMBEDDING_BATCH_SIZE,
    OpenAIEmbeddingModel,
)


class FakeEmbeddingsAPI:

    def __init__(self):
        self.calls: list[list[str]] = []

    def create(self, *, model: str, input: list[str]):
        self.calls.append(list(input))

        entries = [
            SimpleNamespace(
                index=index,
                embedding=[float(text.split("-")[1])],
            )
            for index, text in enumerate(input)
        ]

        return SimpleNamespace(data=list(reversed(entries)))


def build_model() -> tuple[OpenAIEmbeddingModel, FakeEmbeddingsAPI]:

    model = OpenAIEmbeddingModel()
    api = FakeEmbeddingsAPI()

    model.client = SimpleNamespace(embeddings=api)

    return model, api


def make_texts(count: int) -> list[str]:

    return [f"text-{index}" for index in range(count)]


def test_empty_input_returns_without_api_call() -> None:

    model, api = build_model()

    assert model.embed_documents([]) == []
    assert api.calls == []


def test_fewer_texts_than_one_batch_uses_single_call() -> None:

    model, api = build_model()
    texts = make_texts(40)

    embeddings = model.embed_documents(texts)

    assert len(api.calls) == 1
    assert api.calls[0] == texts
    assert len(embeddings) == 40


def test_multiple_batches_use_correct_call_count() -> None:

    model, api = build_model()
    texts = make_texts(250)

    embeddings = model.embed_documents(texts)

    assert len(api.calls) == 3
    assert [len(call) for call in api.calls] == [
        EMBEDDING_BATCH_SIZE,
        EMBEDDING_BATCH_SIZE,
        50,
    ]
    assert [
        text
        for call in api.calls
        for text in call
    ] == texts
    assert len(embeddings) == 250


def test_embeddings_preserve_input_order_across_batches() -> None:

    model, api = build_model()
    texts = make_texts(EMBEDDING_BATCH_SIZE + 5)

    embeddings = model.embed_documents(texts)

    expected = [
        [float(text.split("-")[1])]
        for text in texts
    ]

    assert embeddings == expected


def test_single_embedding_value_matches_its_text() -> None:

    model, api = build_model()

    embeddings = model.embed_documents(
        ["text-7", "text-3", "text-42", "text-0"],
    )

    assert embeddings == [[7.0], [3.0], [42.0], [0.0]]
