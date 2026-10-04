from langchain_core.tools import tool

from app.services.mcp_client_service import (
    get_document_info,
    list_documents,
    search_document,
)


@tool
async def search_document_tool(
    document_id: str,
    query: str,
    k: int = 3,
) -> list[dict]:
    """Search an uploaded document for information relevant to a question."""

    return await search_document(
        document_id,
        query,
        k,
    )


@tool
async def get_document_info_tool(
    document_id: str,
) -> dict:
    """Get information about an uploaded document."""

    return await get_document_info(
        document_id,
    )


@tool
async def list_documents_tool() -> list[dict]:
    """List all uploaded documents."""

    return await list_documents()