from fastapi import APIRouter, HTTPException

from app.models.agent import ChatRequest, ChatResponse, SourceRef
from app.services.agent_service import run_agent


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest) -> ChatResponse:

    user_messages = [
        message
        for message in request.messages
        if message.role == "user"
    ]

    if not user_messages:
        raise HTTPException(
            status_code=400,
            detail="No user message provided.",
        )

    question = user_messages[-1].content.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="User message cannot be empty.",
        )

    last_user_index = max(
        index
        for index, message in enumerate(request.messages)
        if message.role == "user"
    )

    history = request.messages[:last_user_index]

    if not request.document_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one document_id is required.",
        )

    try:
        result = await run_agent(
            question=question,
            document_ids=request.document_ids,
            max_steps=request.max_steps,
            history=history,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {exc}",
        ) from exc

    sources = [
        SourceRef(
            document_id=source["document_id"],
            document_name=source.get("document_name"),
            page=source.get("page"),
            score=source.get("score"),
        )
        for source in result["sources"]
    ]

    return ChatResponse(
        answer=result["answer"],
        traces=result["traces"],
        sources=sources,
    )


@router.get("/tools")
def list_tools() -> dict[str, list[str]]:
    return {
        "tools": [
            "search_document_tool",
            "get_document_info_tool",
            "list_documents_tool",
        ]
    }
