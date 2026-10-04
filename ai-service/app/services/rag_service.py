from app.services.llm_service import generate_answer
from app.services.mcp_client_service import search_document


async def answer_question(
    document_id: str,
    question: str,
    k: int = 3,
) -> dict:

    results = await search_document(
        document_id,
        question,
        k=k,
    )

    if not results:
        return {
            "answer": "I don't know based on the provided document.",
            "sources": [],
        }

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    answer = generate_answer(
        question,
        context,
    )

    sources = [
        {
            "document_id": result["document_id"],
            "page_number": result["page_number"],
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }