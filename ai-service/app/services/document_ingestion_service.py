
from pathlib import Path

from app.core.config import get_settings
from app.services.chunking_service import chunk_pages
from app.services.pdf_service import extract_pages
from app.services.document_metadata_service import save_document_metadata
from app.services.vector_store_service import (
    create_vector_store,
    save_vector_store,
)


def ingest_document(
    document_id: str,
    file_path: Path,
    document_name: str,
) -> None:

    pages = extract_pages(file_path)

    chunks = chunk_pages(pages)

    vector_store = create_vector_store(chunks, document_id)

    settings = get_settings()

    vector_store_path = (
        Path(settings.storage_dir)
        / "vector_stores"
        / document_id
    )

    vector_store_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_vector_store(
        vector_store,
        str(vector_store_path),
    )

    save_document_metadata(
        vector_store_path,
        document_id,
        document_name,
    )
