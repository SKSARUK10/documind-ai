import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from langchain_core.messages import AIMessage

from app.models.agent import ChatMessage
from app.services.agent_service import run_agent


ORIGINAL_QUESTION = "Why is it useful?"
REWRITTEN_QUERY = (
    "Why is Retrieval Augmented Generation (RAG) useful for AI agents?"
)

RETRIEVAL_RESULT = [
    {
        "document_id": "doc-1",
        "document_name": "notes.pdf",
        "page_number": 2,
        "text": "RAG content.",
        "score": 0.9,
    }
]


def test_retrieval_uses_rewritten_query_but_answer_uses_original() -> None:
    search_tool = SimpleNamespace(
        ainvoke=AsyncMock(return_value=RETRIEVAL_RESULT)
    )

    rewrite_llm = Mock()

    async def rewrite_ainvoke(messages):
        return AIMessage(content=REWRITTEN_QUERY)

    rewrite_llm.ainvoke = rewrite_ainvoke

    agent_bound = Mock()

    async def agent_ainvoke(messages):
        agent_bound.messages = messages
        return AIMessage(content="Because it grounds the model.")

    agent_bound.ainvoke = agent_ainvoke

    agent_llm = Mock()
    agent_llm.bind_tools = Mock(return_value=agent_bound)

    history = [
        ChatMessage(role="user", content="What is RAG?"),
        ChatMessage(
            role="assistant",
            content="RAG is Retrieval Augmented Generation.",
        ),
    ]

    with patch(
        "app.services.query_rewrite_service.create_llm",
        return_value=rewrite_llm,
    ), patch(
        "app.services.agent_service.create_llm",
        return_value=agent_llm,
    ), patch(
        "app.services.agent_service.search_document_tool",
        search_tool,
    ):
        result = asyncio.run(
            run_agent(
                question=ORIGINAL_QUESTION,
                document_ids=["doc-1"],
                history=history,
            )
        )

    search_tool.ainvoke.assert_awaited_once_with(
        {
            "document_id": "doc-1",
            "query": REWRITTEN_QUERY,
            "k": 3,
        }
    )

    llm_contents = [
        str(message.content)
        for message in agent_bound.messages
    ]
    assert any(
        ORIGINAL_QUESTION in content
        for content in llm_contents
    )
    assert not any(
        REWRITTEN_QUERY in content
        for content in llm_contents
    )

    assert result["answer"] == "Because it grounds the model."
    assert result["traces"][0]["tool"] == "search_document_tool"
    assert (
        result["traces"][0]["arguments"]["query"]
        == REWRITTEN_QUERY
    )
    assert result["sources"] == [
        {
            "document_id": "doc-1",
            "document_name": "notes.pdf",
            "page": 2,
            "score": 0.9,
        }
    ]


def test_single_turn_retrieval_keeps_original_query() -> None:
    search_tool = SimpleNamespace(
        ainvoke=AsyncMock(return_value=RETRIEVAL_RESULT)
    )

    rewrite_llm = Mock()

    async def rewrite_ainvoke(messages):
        raise AssertionError("rewrite must not run without history")

    rewrite_llm.ainvoke = rewrite_ainvoke

    agent_bound = Mock()

    async def agent_ainvoke(messages):
        return AIMessage(content="answer")

    agent_bound.ainvoke = agent_ainvoke

    agent_llm = Mock()
    agent_llm.bind_tools = Mock(return_value=agent_bound)

    with patch(
        "app.services.query_rewrite_service.create_llm",
        return_value=rewrite_llm,
    ), patch(
        "app.services.agent_service.create_llm",
        return_value=agent_llm,
    ), patch(
        "app.services.agent_service.search_document_tool",
        search_tool,
    ):
        asyncio.run(
            run_agent(
                question="What is RAG?",
                document_ids=["doc-1"],
            )
        )

    search_tool.ainvoke.assert_awaited_once_with(
        {
            "document_id": "doc-1",
            "query": "What is RAG?",
            "k": 3,
        }
    )
