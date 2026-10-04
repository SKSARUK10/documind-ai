import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

server_params = StdioServerParameters(
    command="python",
    args=["-m", "documind_mcp.server"],
)


async def search_document(
    document_id: str,
    query: str,
    k: int = 3,
) -> list[dict]:
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

            return result.structured_content["result"]


async def get_document_info(
    document_id: str,
) -> dict:

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_document_info",
                {
                    "document_id": document_id,
                },
            )

            content = result.content[0]

            if not isinstance(content, TextContent):
                raise ValueError(
                    "Expected text content from get_document_info."
                )

            return json.loads(content.text)

async def list_documents() -> list[dict]:

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "list_documents",
                {},
            )

            return result.structured_content["result"]

async def list_mcp_tools():

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.list_tools()

            return result.tools