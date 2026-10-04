from app.services.vector_store_service import (
    create_vector_store,
    search_vector_store,
)


def test_create_vector_store():
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

    vector_store = create_vector_store(chunks)

    assert vector_store is not None


def test_search_vector_store():
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

    vector_store = create_vector_store(chunks)

    results = search_vector_store(
        vector_store,
        "What is Python?",
        k=1,
    )

    assert len(results) == 1
    assert "Python" in results[0]