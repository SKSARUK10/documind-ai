from unittest.mock import Mock, patch

from app.services.rag_service import answer_question


def test_answer_question():
    mock_vector_store = Mock()

    mock_results = [
        {
            "page_number": 1,
            "text": "Python is a programming language.",
        },
        {
            "page_number": 2,
            "text": "Python is easy to learn.",
        },
    ]

    with patch(
        "app.services.rag_service.search_vector_store",
        return_value=mock_results,
    ) as mock_search, patch(
        "app.services.rag_service.generate_answer",
        return_value="Python is a programming language.",
    ) as mock_generate:

        result = answer_question(
            vector_store=mock_vector_store,
            question="What is Python?",
            k=2,
        )

        assert result["answer"] == "Python is a programming language."

        assert result["sources"] == [
            {"page_number": 1},
            {"page_number": 2},
        ]

        mock_search.assert_called_once_with(
            mock_vector_store,
            "What is Python?",
            k=2,
        )

        mock_generate.assert_called_once_with(
            "What is Python?",
            "Python is a programming language.\n\nPython is easy to learn.",
        )


def test_answer_question_no_results():
    mock_vector_store = Mock()

    with patch(
        "app.services.rag_service.search_vector_store",
        return_value=[],
    ) as mock_search, patch(
        "app.services.rag_service.generate_answer",
    ) as mock_generate:

        result = answer_question(
            vector_store=mock_vector_store,
            question="What is Python?",
        )

        assert result == {
            "answer": "I don't know based on the provided document.",
            "sources": [],
        }

        mock_search.assert_called_once_with(
            mock_vector_store,
            "What is Python?",
            k=3,
        )

        mock_generate.assert_not_called()