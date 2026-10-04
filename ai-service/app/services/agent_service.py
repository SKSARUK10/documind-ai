import logging

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    ToolMessage,
)

from app.models.agent import ChatMessage
from app.services.llm_service import create_llm
from app.services.mcp_tools import (
    get_document_info_tool,
    list_documents_tool,
    search_document_tool,
)
from app.services.query_rewrite_service import (
    create_standalone_query,
)


logger = logging.getLogger("documind.ai")


TOOLS = [
    search_document_tool,
    get_document_info_tool,
    list_documents_tool,
]

TOOLS_BY_NAME = {
    tool.name: tool
    for tool in TOOLS
}


def add_source(
    sources: list[dict],
    item: dict,
) -> None:

    source = {
        "document_id": item["document_id"],
        "document_name": item.get("document_name"),
        "page": item["page_number"],
        "score": item.get("score"),
    }

    if source not in sources:
        sources.append(source)


def extract_error(
    result: object,
) -> str | None:

    if isinstance(result, dict) and "error" in result:
        return str(result["error"])

    if isinstance(result, list):

        for item in result:

            if isinstance(item, dict) and "error" in item:
                return str(item["error"])

    return None


def history_to_messages(
    history: list[ChatMessage] | None,
) -> list[AnyMessage]:

    messages: list[AnyMessage] = []

    for entry in history or []:

        if not entry.content.strip():
            continue

        if entry.role == "user":
            messages.append(
                HumanMessage(
                    content=entry.content
                )
            )

        elif entry.role == "assistant":
            messages.append(
                AIMessage(
                    content=entry.content
                )
            )

    return messages


async def run_agent(
    question: str,
    document_ids: list[str],
    max_steps: int = 5,
    history: list[ChatMessage] | None = None,
) -> dict:

    llm = create_llm()
    llm_with_tools = llm.bind_tools(TOOLS)

    history_messages = history_to_messages(
        history
    )

    messages: list[AnyMessage] = list(history_messages)

    messages.append(
        HumanMessage(
            content=question
        )
    )

    traces = []
    sources = []

    # Always search all selected documents first.
    if document_ids:

        retrieval_query = await create_standalone_query(
            question,
            history_messages,
        )

        retrieved_contexts = []

        for document_id in document_ids:

            search_args = {
                "document_id": document_id,
                "query": retrieval_query,
                "k": 3,
            }

            try:
                result = await search_document_tool.ainvoke(
                    search_args
                )

            except Exception as exc:
                logger.exception(
                    "search_document_tool failed for document %s",
                    document_id,
                )
                result = {"error": str(exc)}

            error = extract_error(result)

            if isinstance(result, list):

                for item in result:

                    if (
                        isinstance(item, dict)
                        and "document_id" in item
                        and "page_number" in item
                    ):
                        add_source(sources, item)

            traces.append(
                {
                    "tool": "search_document_tool",
                    "arguments": search_args,
                    "result_summary": str(result)[:500],
                    "ok": error is None,
                }
            )

            retrieved_contexts.append(
                f"Document ID: {document_id}\n"
                f"Retrieved context:\n{result}"
            )

        messages.append(
            HumanMessage(
                content=(
                    "Use the following retrieved document contexts "
                    "to answer the question. Consider information from "
                    "all selected documents. Do not use your general "
                    "knowledge when the answer is not present in these "
                    "contexts.\n\n"
                    + "\n\n---\n\n".join(retrieved_contexts)
                )
            )
        )

    for _ in range(max_steps):

        response = await llm_with_tools.ainvoke(messages)

        messages.append(response)

        if not response.tool_calls:
            return {
                "answer": str(response.content),
                "traces": traces,
                "sources": sources,
            }

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if (
                tool_name == "search_document_tool"
                and not tool_args.get("document_id")
            ):
                if not document_ids:
                    raise ValueError(
                        "No document_id available for document search."
                    )

                tool_args["document_id"] = document_ids[0]

            tool = TOOLS_BY_NAME.get(tool_name)
            error: str | None = None

            if tool is None:
                error = f"Unknown tool: {tool_name}"
                result = error

            else:
                try:
                    result = await tool.ainvoke(tool_args)

                except Exception as exc:
                    logger.exception(
                        "Tool %s failed",
                        tool_name,
                    )
                    error = str(exc)
                    result = f"Tool call failed: {exc}"

            if error is None:
                error = extract_error(result)

            if tool_name == "search_document_tool":

                if isinstance(result, list):

                    for item in result:

                        if (
                            isinstance(item, dict)
                            and "document_id" in item
                            and "page_number" in item
                        ):
                            add_source(sources, item)

            traces.append(
                {
                    "tool": tool_name,
                    "arguments": tool_args,
                    "result_summary": str(result)[:500],
                    "ok": error is None,
                }
            )

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

    traces.append(
        {
            "tool": "agent_loop",
            "arguments": {"max_steps": max_steps},
            "result_summary": (
                "Agent reached max_steps before producing a "
                "final answer."
            ),
            "ok": False,
        }
    )

    return {
        "answer": (
            "I could not finish answering within the allowed "
            "number of steps. Please try again or ask a more "
            "specific question."
        ),
        "traces": traces,
        "sources": sources,
    }