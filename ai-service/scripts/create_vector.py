from pathlib import Path

from app.services.chunking_service import chunk_pages
from app.services.pdf_service import extract_pages
from app.services.vector_store_service import (
    create_vector_store,
    save_vector_store,
)


BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "tests" / "fixtures" / "sample.pdf"
VECTOR_STORE_PATH = BASE_DIR / "data" / "vector_store"


def main() -> None:
    print(f"Reading PDF: {PDF_PATH}")

    pages = extract_pages(PDF_PATH)

    print(f"Extracted {len(pages)} pages")

    chunks = chunk_pages(pages)

    print(f"Created {len(chunks)} chunks")

    vector_store = create_vector_store(chunks)

    VECTOR_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_vector_store(
        vector_store,
        str(VECTOR_STORE_PATH),
    )

    print(f"Vector store saved to: {VECTOR_STORE_PATH}")


if __name__ == "__main__":
    main()