
import json
from pathlib import Path


def save_document_metadata(
    vector_store_path: Path,
    document_id: str,
    document_name: str,
) -> None:
    metadata = {
        "document_id": document_id,
        "document_name": document_name,
    }

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
