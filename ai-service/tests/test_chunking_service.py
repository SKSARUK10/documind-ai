from app.services.chunking_service import chunk_pages


def test_chunk_pages():
    pages = [
        {
            "page_number": 1,
            "text": "This is a sample document with some text."
        }
    ]

    chunks = chunk_pages(pages)

    assert len(chunks) == 1
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["text"] != ""


def test_chunk_long_text():
    pages = [
        {
            "page_number": 1,
            "text": "A" * 1200
        }
    ]

    chunks = chunk_pages(pages)

    assert len(chunks) > 1

    for chunk in chunks:
        assert chunk["page_number"] == 1
        assert chunk["text"] != ""