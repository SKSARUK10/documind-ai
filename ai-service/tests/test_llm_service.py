from unittest.mock import patch

from app.core.config import get_settings
from app.services.llm_service import (
    OpenAIChatModel,
    create_llm,
    generate_answer,
)


def test_create_llm():
    with patch("app.services.llm_service.OpenAI"), patch(
        "app.services.llm_service.AsyncOpenAI",
    ):
        llm = create_llm()

    assert isinstance(llm, OpenAIChatModel)
    assert llm.model == get_settings().llm_model


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