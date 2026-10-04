import asyncio

from app.services.mcp_tools import list_documents_tool


async def main() -> None:

    result = await list_documents_tool.ainvoke({})

    print("TOOL RESULT:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())