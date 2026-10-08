import json
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from app.services import document_ingestion_service as ingestion
from app.services.document_ingestion_service import (
    DocumentProcessingError,
    ingest_document,
)


CSV_CONTENT = (
    "name,department,salary\n"
    "Alice,Engineering,80000\n"
    "Bob,Sales,60000\n"
)


def configure_storage(
    tmp_path: Path,
    monkeypatch,
) -> Path:

    storage_dir = tmp_path / "storage"

    settings = SimpleNamespace(
        storage_dir=str(storage_dir),
    )

    monkeypatch.setattr(
        ingestion,
        "get_settings",
        lambda: settings,
    )

    return storage_dir


def stub_vector_store(
    monkeypatch,
) -> list[dict]:
    """Skip network calls, capture the chunks handed to FAISS."""

    captured: list[dict] = []

    def fake_create_vector_store(chunks, document_id):
        captured.extend(chunks)
        return object()

    monkeypatch.setattr(
        ingestion,
        "create_vector_store",
        fake_create_vector_store,
    )
    monkeypatch.setattr(
        ingestion,
        "save_vector_store",
        lambda vector_store, path: None,
    )

    return captured


def read_metadata(storage_dir: Path, document_id: str) -> dict:
    metadata_path = (
        storage_dir
        / "vector_stores"
        / document_id
        / "metadata.json"
    )

    with metadata_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_csv_ingestion_writes_file_type_metadata(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)
    chunks = stub_vector_store(monkeypatch)

    csv_path = tmp_path / "employees.csv"
    csv_path.write_text(CSV_CONTENT, encoding="utf-8")

    ingest_document("doc-1", csv_path, "employees.csv")

    metadata = read_metadata(storage_dir, "doc-1")

    assert metadata["document_id"] == "doc-1"
    assert metadata["document_name"] == "employees.csv"
    assert metadata["file_type"] == "csv"

    assert chunks
    assert all("page_number" in chunk for chunk in chunks)
    assert any(
        "name: Alice | department: Engineering | salary: 80000"
        in chunk["text"]
        for chunk in chunks
    )


def test_excel_ingestion_keeps_sheet_names_in_chunks(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)
    chunks = stub_vector_store(monkeypatch)

    workbook_path = tmp_path / "sales.xlsx"

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        pd.DataFrame(
            {"name": ["Alice"], "salary": [80000]}
        ).to_excel(
            writer,
            sheet_name="Employees",
            index=False,
        )
        pd.DataFrame(
            {"region": ["North"], "target": [120000]}
        ).to_excel(
            writer,
            sheet_name="Targets",
            index=False,
        )

    ingest_document("doc-2", workbook_path, "sales.xlsx")

    metadata = read_metadata(storage_dir, "doc-2")
    assert metadata["file_type"] == "xlsx"

    assert any(
        chunk.get("sheet_name") == "Employees"
        for chunk in chunks
    )
    assert any(
        chunk.get("sheet_name") == "Targets"
        for chunk in chunks
    )
    assert any(
        "Sheet: Employees" in chunk["text"]
        for chunk in chunks
    )


def test_empty_csv_ingestion_raises_processing_error(
    tmp_path: Path,
    monkeypatch,
) -> None:

    configure_storage(tmp_path, monkeypatch)

    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")

    with pytest.raises(DocumentProcessingError) as error:
        ingest_document("doc-3", csv_path, "empty.csv")

    assert "does not contain any readable data" in str(error.value)
    assert "Traceback" not in str(error.value)
