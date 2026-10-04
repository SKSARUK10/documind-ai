import asyncio

from app.services.mcp_tools import (
    get_document_info_tool,
    list_documents_tool,
    search_document_tool,
)


async def test() -> None:

    print("Search tool:")
    print(search_document_tool.name)
    print(search_document_tool.description)

    print("\nInfo tool:")
    print(get_document_info_tool.name)
    print(get_document_info_tool.description)

    print("\nList tool:")
    print(list_documents_tool.name)
    print(list_documents_tool.description)

    print("\nList documents result:")
    result = await list_documents_tool.ainvoke({})

    print(result)


if __name__ == "__main__":
    asyncio.run(test())