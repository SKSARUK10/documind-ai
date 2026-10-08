
from pathlib import Path

from app.core.config import get_settings
from app.services.chunking_service import chunk_pages
from app.services.text_extraction_service import (
    TextExtractionError,
    extract_pages_for_file,
)
from app.services.document_metadata_service import save_document_metadata
from app.services.vector_store_service import (
    create_vector_store,
    save_vector_store,
)


class DocumentProcessingError(Exception):
    """The uploaded document cannot be converted into a vector store."""


def ingest_document(
    document_id: str,
    file_path: Path,
    document_name: str,
) -> None:

    extension = file_path.suffix.lower()

    try:
        pages = extract_pages_for_file(
            file_path,
            extension,
        )
    except TextExtractionError as exc:
        raise DocumentProcessingError(
            str(exc),
        ) from None

    chunks = chunk_pages(pages)

    chunks = [
        chunk
        for chunk in chunks
        if chunk["text"].strip()
    ]

    if not chunks:
        raise DocumentProcessingError(
            "The uploaded document does not contain any readable text.",
        )

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
        file_type=extension.lstrip("."),
    )
