import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["-m", "documind_mcp.server"],
)


async def search_document(
    document_id: str,
    query: str,
    k: int = 3,
):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "search_document",
                {
                    "document_id": document_id,
                    "query": query,
                    "k": k,
                },
            )

            return result


async def main() -> None:

    document_id = "436e7a67-ff3a-4e10-9d76-de3ee94f2e15"
    query = "What topics are covered in Module 7 about RAG?"

    result = await search_document(
        document_id,
        query,
    )

    print("\nSearch result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())