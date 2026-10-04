import asyncio

from app.services.mcp_client_service import list_mcp_tools


async def test() -> None:

    tools = await list_mcp_tools()

    for tool in tools:
        print("\nTool:", tool.name)
        print("Description:", tool.description)
        print("Input schema:", tool.model_dump().get("inputSchema"))


if __name__ == "__main__":
    asyncio.run(test())