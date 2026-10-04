import asyncio
from unittest.mock import Mock, patch

from langchain_core.messages import AIMessage

from app.models.agent import ChatMessage
from app.services.agent_service import history_to_messages
from app.services.query_rewrite_service import create_standalone_query


FOLLOW_UP = "Why is it useful?"
REWRITTEN = (
    "Why is Retrieval Augmented Generation (RAG) useful for AI agents?"
)

HISTORY = [
    ChatMessage(role="user", content="What is RAG?"),
    ChatMessage(
        role="assistant",
        content="RAG is Retrieval Augmented Generation.",
    ),
]


def test_standalone_question_is_not_rewritten() -> None:
    with patch(
        "app.services.query_rewrite_service.create_llm"
    ) as mock_create_llm:
        result = asyncio.run(
            create_standalone_query("What is RAG?", [])
        )

    assert result == "What is RAG?"
    mock_create_llm.assert_not_called()


def test_follow_up_is_rewritten_with_history() -> None:
    captured = {}

    fake_llm = Mock()

    async def fake_ainvoke(messages):
        captured["messages"] = messages
        return AIMessage(content=REWRITTEN)

    fake_llm.ainvoke = fake_ainvoke

    with patch(
        "app.services.query_rewrite_service.create_llm",
        return_value=fake_llm,
    ):
        result = asyncio.run(
            create_standalone_query(
                FOLLOW_UP,
                history_to_messages(HISTORY),
            )
        )

    assert result == REWRITTEN

    contents = [
        str(message.content)
        for message in captured["messages"]
    ]
    assert "What is RAG?" in contents
    assert "RAG is Retrieval Augmented Generation." in contents
    assert any(
        FOLLOW_UP in content for content in contents
    )
    assert "standalone search query" in contents[0]


def test_rewrite_failure_falls_back_to_original_question() -> None:
    fake_llm = Mock()

    async def failing_ainvoke(messages):
        raise RuntimeError("rewrite failed")

    fake_llm.ainvoke = failing_ainvoke

    with patch(
        "app.services.query_rewrite_service.create_llm",
        return_value=fake_llm,
    ):
        result = asyncio.run(
            create_standalone_query(
                FOLLOW_UP,
                history_to_messages(HISTORY),
            )
        )

    assert result == FOLLOW_UP


def test_empty_rewrite_output_falls_back_to_original_question() -> None:
    fake_llm = Mock()

    async def empty_ainvoke(messages):
        return AIMessage(content="   ")

    fake_llm.ainvoke = empty_ainvoke

    with patch(
        "app.services.query_rewrite_service.create_llm",
        return_value=fake_llm,
    ):
        result = asyncio.run(
            create_standalone_query(
                FOLLOW_UP,
                history_to_messages(HISTORY),
            )
        )

    assert result == FOLLOW_UP
