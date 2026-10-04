from langchain_core.documents import Document

from app.services.vector_store_service import (
    MAX_RELEVANT_SCORE,
    SCORE_MARGIN,
    filter_relevant_results,
    search_vector_store,
)


class FakeDocstore:
    def __init__(self, documents: list[Document]) -> None:
        self._dict = {
            str(index): document
            for index, document in enumerate(documents)
        }


class FakeVectorStore:
    def __init__(
        self,
        documents: list[Document],
        scores: list[float],
    ) -> None:
        self.documents = documents
        self.scores = scores
        self.docstore = FakeDocstore(documents)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3,
    ) -> list[tuple[Document, float]]:
        return list(
            zip(
                self.documents[:k],
                self.scores[:k],
            )
        )


def make_documents(count: int) -> list[Document]:
    return [
        Document(
            page_content=f"chunk {index}",
            metadata={
                "document_id": "doc-1",
                "page_number": index + 1,
                "chunk_index": index,
            },
        )
        for index in range(count)
    ]


# Scores below are real measurements against the stored indexes.
RELEVANT_A = [1.3083, 1.3916, 1.5983]      # "What is RAG?" (course doc)
RELEVANT_FOLLOW_UP = [1.1521, 1.1587, 1.1597]  # contextual follow-up
UNRELATED = [1.7168, 1.7668, 1.7988]       # "hiking trails in the Alps"


def test_relevant_semantic_query_is_kept() -> None:
    store = FakeVectorStore(make_documents(3), RELEVANT_A)

    results = search_vector_store(store, "What is RAG?", k=3)

    assert [result["score"] for result in results] == RELEVANT_A[:2]

    # Regression: the previous `score <= 1.2` rule rejected every
    # candidate of this query.
    old_rule = [score for score in RELEVANT_A if score <= 1.2]
    assert old_rule == []


def test_relevant_follow_up_query_is_kept() -> None:
    store = FakeVectorStore(
        make_documents(3),
        RELEVANT_FOLLOW_UP,
    )

    results = search_vector_store(
        store,
        "Why is Retrieval Augmented Generation (RAG) useful for AI agents?",
        k=3,
    )

    assert [result["score"] for result in results] == RELEVANT_FOLLOW_UP


def test_clearly_unrelated_query_returns_nothing() -> None:
    store = FakeVectorStore(make_documents(3), UNRELATED)

    results = search_vector_store(
        store,
        "Best hiking trails in the Alps during autumn",
        k=3,
    )

    assert results == []


def test_module_query_uses_deterministic_path_without_score() -> None:
    documents = [
        Document(
            page_content="Module 7: RAG with FAISS.",
            metadata={
                "document_id": "doc-1",
                "page_number": 2,
                "chunk_index": 0,
            },
        ),
        Document(
            page_content="Continuation of module 7 content.",
            metadata={
                "document_id": "doc-1",
                "page_number": 2,
                "chunk_index": 1,
            },
        ),
    ]
    store = FakeVectorStore(documents, UNRELATED)

    results = search_vector_store(
        store,
        "What topics are covered in Module 7 about RAG?",
        k=3,
    )

    assert [result["page_number"] for result in results] == [2, 2]
    assert all(result["score"] is None for result in results)


def test_multi_document_retrieval_is_independent() -> None:
    first = FakeVectorStore(make_documents(3), RELEVANT_A)
    second = FakeVectorStore(make_documents(3), RELEVANT_FOLLOW_UP)
    unrelated = FakeVectorStore(make_documents(3), UNRELATED)

    assert search_vector_store(first, "What is RAG?", k=3)
    assert search_vector_store(
        second,
        "What is retrieval augmented generation?",
        k=3,
    )
    assert search_vector_store(
        unrelated,
        "Best hiking trails in the Alps during autumn",
        k=3,
    ) == []


def test_score_metadata_is_the_raw_faiss_distance() -> None:
    store = FakeVectorStore(make_documents(3), RELEVANT_A)

    results = search_vector_store(store, "What is RAG?", k=3)

    for result, expected in zip(results, RELEVANT_A[:2]):
        assert set(result) == {
            "document_id",
            "page_number",
            "text",
            "score",
        }
        assert result["document_id"] == "doc-1"
        assert isinstance(result["score"], float)
        assert result["score"] == expected


def test_empty_retrieval_returns_empty_list() -> None:
    store = FakeVectorStore([], [])

    assert search_vector_store(store, "What is RAG?", k=3) == []
    assert filter_relevant_results([]) == []


def test_threshold_replacement_rules() -> None:
    documents = make_documents(4)

    # Above the old 1.2 limit but inside the measured topical band.
    kept = filter_relevant_results(
        list(zip(documents[:1], [1.25]))
    )
    assert len(kept) == 1

    # Above the new absolute ceiling.
    rejected = filter_relevant_results(
        list(zip(documents[:1], [MAX_RELEVANT_SCORE + 0.01]))
    )
    assert rejected == []

    # Relative rule: a weak tail far behind a strong best is dropped.
    tail = filter_relevant_results(
        list(zip(documents, [0.4, 0.9, 1.4, 1.5]))
    )
    assert [score for _, score in tail] == [0.4, 0.9]
    assert SCORE_MARGIN == 0.6
    assert MAX_RELEVANT_SCORE == 1.5
