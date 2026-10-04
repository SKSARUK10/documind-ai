import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from langchain_core.messages import AIMessage, ToolMessage

from app.services.agent_service import run_agent


DOC = "doc-1"


def make_agent(responses: list[AIMessage]):
    bound = Mock()
    bound.seen = []
    state = {"count": 0}

    async def ainvoke(messages):
        bound.seen.append(list(messages))
        index = min(state["count"], len(responses) - 1)
        state["count"] += 1
        return responses[index]

    bound.ainvoke = ainvoke

    llm = Mock()
    llm.bind_tools = Mock(return_value=bound)
    return llm, bound


def tool_call(name: str, args: dict, call_id: str = "call-1") -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": name,
                "args": args,
                "id": call_id,
                "type": "tool_call",
            }
        ],
    )


def run(question, llm, document_ids=None, max_steps=5, search_result=None):
    search_tool = SimpleNamespace(
        ainvoke=AsyncMock(
            return_value=[] if search_result is None else search_result
        )
    )
    with patch(
        "app.services.agent_service.create_llm",
        return_value=llm,
    ), patch(
        "app.services.agent_service.search_document_tool",
        search_tool,
    ):
        return asyncio.run(
            run_agent(
                question=question,
                document_ids=document_ids or [DOC],
                max_steps=max_steps,
            )
        )


def test_max_steps_is_respected_and_returns_safe_response() -> None:
    always_call = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "list_documents_tool",
                "args": {},
                "id": "call-1",
                "type": "tool_call",
            }
        ],
    )
    llm, bound = make_agent([always_call])

    with patch(
        "app.services.agent_service.TOOLS_BY_NAME",
        {
            "list_documents_tool": SimpleNamespace(
                ainvoke=AsyncMock(return_value=[])
            )
        },
    ):
        result = run("Hello", llm, max_steps=2)

    assert len(bound.seen) == 2
    assert result["answer"].startswith("I could not finish answering")
    assert result["traces"][-1]["tool"] == "agent_loop"
    assert result["traces"][-1]["ok"] is False
    assert result["traces"][-1]["arguments"] == {"max_steps": 2}
    assert any(
        trace["tool"] == "list_documents_tool"
        for trace in result["traces"]
    )


def test_tool_failure_is_recorded_and_agent_recovers() -> None:
    responses = [
        tool_call(
            "search_document_tool",
            {"document_id": DOC, "query": "What is RAG?"},
        ),
        AIMessage(content="I could not search the document."),
    ]
    llm, bound = make_agent(responses)

    failing_tool = SimpleNamespace(
        ainvoke=AsyncMock(side_effect=RuntimeError("MCP server crashed"))
    )

    with patch(
        "app.services.agent_service.TOOLS_BY_NAME",
        {"search_document_tool": failing_tool},
    ):
        result = run("What is RAG?", llm)

    assert result["answer"] == "I could not search the document."
    assert result["traces"][-1]["ok"] is False
    assert result["traces"][-1]["tool"] == "search_document_tool"
    assert "MCP server crashed" in result["traces"][-1]["result_summary"]

    second_call_messages = bound.seen[-1]
    tool_messages = [
        message
        for message in second_call_messages
        if isinstance(message, ToolMessage)
    ]
    assert tool_messages
    assert "Tool call failed" in tool_messages[0].content
    assert tool_messages[0].tool_call_id == "call-1"


def test_invalid_document_reports_failed_trace() -> None:
    llm, _ = make_agent([AIMessage(content="That document was not found.")])

    result = run(
        "What is RAG?",
        llm,
        document_ids=["does-not-exist"],
        search_result={
            "error": "Document vector store not found.",
            "document_id": "does-not-exist",
        },
    )

    assert result["traces"][0]["ok"] is False
    assert (
        "Document vector store not found."
        in result["traces"][0]["result_summary"]
    )
    assert result["sources"] == []
    assert result["answer"] == "That document was not found."


def test_mcp_list_wrapped_error_reports_failed_trace() -> None:
    # The MCP server returns missing-store errors inside a list.
    llm, _ = make_agent([AIMessage(content="That document was not found.")])

    result = run(
        "What is RAG?",
        llm,
        document_ids=["does-not-exist"],
        search_result=[
            {
                "error": "Document vector store not found.",
                "document_id": "does-not-exist",
            }
        ],
    )

    assert result["traces"][0]["ok"] is False
    assert result["sources"] == []


def test_empty_retrieval_stays_grounded() -> None:
    llm, _ = make_agent(
        [AIMessage(content="The document does not cover that topic.")]
    )

    result = run("Best hiking trails in the Alps", llm, search_result=[])

    assert result["traces"][0]["ok"] is True
    assert result["sources"] == []
    assert result["answer"] == "The document does not cover that topic."


def test_casual_question_makes_no_loop_tool_calls() -> None:
    llm, _ = make_agent([AIMessage(content="Hello! How can I help?")])

    result = run("Hello", llm)

    assert result["answer"] == "Hello! How can I help?"
    assert len(result["traces"]) == 1
    assert result["traces"][0]["tool"] == "search_document_tool"


def test_tool_result_is_forwarded_to_the_llm() -> None:
    responses = [
        tool_call("list_documents_tool", {}),
        AIMessage(content="Two documents are uploaded."),
    ]
    llm, bound = make_agent(responses)

    documents = [{"document_id": "d1", "document_name": "notes.pdf"}]

    with patch(
        "app.services.agent_service.TOOLS_BY_NAME",
        {
            "list_documents_tool": SimpleNamespace(
                ainvoke=AsyncMock(return_value=documents)
            )
        },
    ):
        result = run("What documents are uploaded?", llm)

    assert result["answer"] == "Two documents are uploaded."
    assert result["traces"][-1]["ok"] is True

    second_call_messages = bound.seen[-1]
    tool_messages = [
        message
        for message in second_call_messages
        if isinstance(message, ToolMessage)
    ]
    assert len(tool_messages) == 1
    assert str(documents) in tool_messages[0].content
    assert tool_messages[0].tool_call_id == "call-1"


def test_unknown_tool_recovers_with_failed_trace() -> None:
    responses = [
        tool_call("bogus_tool", {}),
        AIMessage(content="That tool is not available."),
    ]
    llm, _ = make_agent(responses)

    result = run("Hello", llm)

    assert result["answer"] == "That tool is not available."
    assert result["traces"][-1]["ok"] is False
    assert (
        "Unknown tool: bogus_tool"
        in result["traces"][-1]["result_summary"]
    )


def test_traces_sources_and_no_internal_prompt_exposure() -> None:
    search_results = [
        {
            "document_id": DOC,
            "document_name": "notes.pdf",
            "page_number": 2,
            "text": "RAG content.",
            "score": 0.9,
        }
    ]
    llm, _ = make_agent([AIMessage(content="Grounded answer.")])

    result = run("What is RAG?", llm, search_result=search_results)

    assert result["sources"] == [
        {
            "document_id": DOC,
            "document_name": "notes.pdf",
            "page": 2,
            "score": 0.9,
        }
    ]
    assert result["traces"][0]["ok"] is True
    assert result["traces"][0]["arguments"]["query"] == "What is RAG?"
    assert {"tool", "arguments", "result_summary", "ok"} <= set(
        result["traces"][0]
    )

    exported = str(result["traces"]) + str(result["answer"])
    assert "Use the following retrieved document contexts" not in exported
    assert "standalone search query" not in exported
