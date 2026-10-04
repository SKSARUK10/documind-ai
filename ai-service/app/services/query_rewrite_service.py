import logging

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
)

from app.services.llm_service import create_llm


logger = logging.getLogger("documind.ai")


REWRITE_SYSTEM_PROMPT = """You rewrite the latest user question into a single standalone search query for document retrieval.

Rules:
- Resolve pronouns and references using the conversation history.
- Preserve the original topic, including module numbers and named concepts.
- Do NOT answer the question.
- Do NOT add information that is not present in the conversation.
- If the question is already standalone, return it unchanged.
- Output only the search query, with no quotes, labels or explanation."""


async def create_standalone_query(
    question: str,
    history: list[AnyMessage],
) -> str:

    if not history:
        return question

    messages: list[AnyMessage] = [
        SystemMessage(
            content=REWRITE_SYSTEM_PROMPT
        )
    ]

    messages.extend(history)

    messages.append(
        HumanMessage(
            content=(
                "Rewrite this latest question as a standalone "
                "search query:\n"
                + question
            )
        )
    )

    try:
        response = await create_llm().ainvoke(messages)

    except Exception:
        logger.exception(
            "Query rewriting failed; using original question."
        )
        return question

    rewritten = str(response.content).strip()

    if not rewritten:
        return question

    return rewritten
