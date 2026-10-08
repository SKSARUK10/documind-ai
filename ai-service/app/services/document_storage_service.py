from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


def save_document(
    file: UploadFile,
    extension: str,
) -> tuple[str, Path]:
    settings = get_settings()

    storage_dir = Path(settings.storage_dir)/"documents"
    storage_dir.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid4())

    file_path = storage_dir/ f"{document_id}{extension}"

    with file_path.open("wb") as output_file:
        while chunk :=file.file.read(1024 * 1024):
            output_file.write(chunk)

    return document_id, file_path
