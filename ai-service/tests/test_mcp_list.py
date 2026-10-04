import asyncio

from app.services.mcp_client_service import list_documents


async def test() -> None:

    result = await list_documents()

    print(result)


if __name__ == "__main__":
    asyncio.run(test())