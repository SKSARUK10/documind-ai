
import json
from pathlib import Path


def save_document_metadata(
    vector_store_path: Path,
    document_id: str,
    document_name: str,
    file_type: str | None = None,
) -> None:
    metadata = {
        "document_id": document_id,
        "document_name": document_name,
    }

    if file_type:
        metadata["file_type"] = file_type

    metadata_path = vector_store_path / "metadata.json"

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def load_document_metadata(
    vector_store_path: Path,
) -> dict:
    metadata_path = vector_store_path / "metadata.json"

    if not metadata_path.exists():
        return {}

    with metadata_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def list_document_metadata(
    vector_stores_path: Path,
) -> list[dict]:

    if not vector_stores_path.exists():
        return []

    documents = []

    for document_path in vector_stores_path.iterdir():
        if not document_path.is_dir():
            continue

        metadata = load_document_metadata(document_path)

        if metadata:
            documents.append(metadata)

    return documents
