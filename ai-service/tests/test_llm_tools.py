from app.services.llm_service import create_llm
from app.services.mcp_tools import (
    get_document_info_tool,
    list_documents_tool,
    search_document_tool,
)


def main() -> None:

    llm = create_llm()

    tools = [
        search_document_tool,
        get_document_info_tool,
        list_documents_tool,
    ]

    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(
        "What documents have I uploaded?"
    )

    print("CONTENT:")
    print(response.content)

    print("\nTOOL CALLS:")
    print(response.tool_calls)


if __name__ == "__main__":
    main()