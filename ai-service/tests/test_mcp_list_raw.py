import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["-m", "documind_mcp.server"],
)


async def test() -> None:

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "list_documents",
                {},
            )

            print("RAW RESULT:")
            print(result)

            print("\nCONTENT:")
            print(result.content)

            print("\nSTRUCTURED CONTENT:")
            print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(test())