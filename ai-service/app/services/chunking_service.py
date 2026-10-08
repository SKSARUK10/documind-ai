from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pages(
    pages: list[dict],
) -> list[dict]:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = []

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        page_chunks = text_splitter.split_text(text)

        for chunk in page_chunks:

            chunk_entry = {
                "page_number": page_number,
                "text": chunk,
            }

            if "sheet_name" in page:
                chunk_entry["sheet_name"] = page["sheet_name"]

            chunks.append(chunk_entry)

    return chunks
