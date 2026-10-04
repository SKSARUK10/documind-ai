from unittest.mock import patch

from app.services.llm_service import create_llm, generate_answer


def test_create_llm():
    with patch("app.services.llm_service.ChatOpenAI") as mock_llm:
        create_llm()

        mock_llm.assert_called_once()

        kwargs = mock_llm.call_args.kwargs

        assert "api_key" in kwargs
        assert "model" in kwargs
        assert "base_url" in kwargs


def test_generate_answer():
    mock_response = type(
        "MockResponse",
        (),
        {"content": "Python is a programming language."},
    )()

    with patch("app.services.llm_service.create_llm") as mock_create_llm:
        mock_llm = mock_create_llm.return_value
        mock_llm.invoke.return_value = mock_response

        result = generate_answer(
            "What is Python?",
            "Python is a programming language.",
        )

        assert result == "Python is a programming language."
        mock_llm.invoke.assert_called_once()