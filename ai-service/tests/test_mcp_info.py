import asyncio

from app.services.mcp_client_service import get_document_info


async def test() -> None:

    result = await get_document_info(
        "436e7a67-ff3a-4e10-9d76-de3ee94f2e15"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(test())