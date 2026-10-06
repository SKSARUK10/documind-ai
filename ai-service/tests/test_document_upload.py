from pathlib import Path
from types import SimpleNamespace

from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app
from app.api.routes import documents as documents_route
from app.services import document_storage_service

client = TestClient(app)


def configure_storage(
    tmp_path: Path,
    monkeypatch,
) -> Path:

    storage_dir = tmp_path / "storage"

    settings = SimpleNamespace(
        storage_dir=str(storage_dir),
    )

    monkeypatch.setattr(
        documents_route,
        "get_settings",
        lambda: settings,
    )
    monkeypatch.setattr(
        document_storage_service,
        "get_settings",
        lambda: settings,
    )

    return storage_dir


def write_blank_pdf(path: Path) -> Path:

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)

    with path.open("wb") as file:
        writer.write(file)

    return path


def upload(pdf_path: Path):
    with pdf_path.open("rb") as file:
        return client.post(
            "/documents/upload",
            files={
                "file": (pdf_path.name, file, "application/pdf"),
            },
        )


def assert_no_orphans(storage_dir: Path) -> None:

    documents_path = storage_dir / "documents"
    vector_stores_path = storage_dir / "vector_stores"

    leftover_documents = (
        list(documents_path.iterdir())
        if documents_path.exists()
        else []
    )

    leftover_vector_stores = (
        list(vector_stores_path.iterdir())
        if vector_stores_path.exists()
        else []
    )

    assert leftover_documents == []
    assert leftover_vector_stores == []


def test_valid_upload_returns_document_response(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)

    monkeypatch.setattr(
        documents_route,
        "ingest_document",
        lambda document_id, file_path, document_name: None,
    )

    response = upload(Path("tests/fixtures/sample.pdf"))

    assert response.status_code == 200
    assert set(response.json()) == {"document_id", "document_name"}
    assert response.json()["document_name"] == "sample.pdf"

    saved_documents = list(
        (storage_dir / "documents").iterdir()
    )
    assert len(saved_documents) == 1


def test_corrupt_pdf_returns_400_and_cleans_up(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)

    corrupt_pdf = tmp_path / "corrupt.pdf"
    corrupt_pdf.write_bytes(b"this is not a pdf file")

    response = upload(corrupt_pdf)

    assert response.status_code == 400
    assert response.headers["content-type"].startswith(
        "application/json"
    )

    detail = response.json()["detail"]
    assert "could not be read" in detail
    assert "Traceback" not in detail
    assert str(tmp_path) not in detail

    assert_no_orphans(storage_dir)


def test_blank_pdf_returns_400_and_cleans_up(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)

    blank_pdf = write_blank_pdf(tmp_path / "blank.pdf")

    response = upload(blank_pdf)

    assert response.status_code == 400

    detail = response.json()["detail"]
    assert "does not contain any readable text" in detail

    assert_no_orphans(storage_dir)


def test_failed_ingestion_returns_500_and_cleans_up(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)

    def fail_ingestion(
        document_id: str,
        file_path: Path,
        document_name: str,
    ) -> None:
        raise RuntimeError("embedding provider exploded")

    monkeypatch.setattr(
        documents_route,
        "ingest_document",
        fail_ingestion,
    )

    response = upload(Path("tests/fixtures/sample.pdf"))

    assert response.status_code == 500

    detail = response.json()["detail"]
    assert detail == (
        "Document processing failed. Please try again later."
    )
    assert "embedding provider exploded" not in detail

    assert_no_orphans(storage_dir)


def test_non_pdf_upload_is_rejected_before_saving(
    tmp_path: Path,
    monkeypatch,
) -> None:

    storage_dir = configure_storage(tmp_path, monkeypatch)

    text_file = tmp_path / "notes.txt"
    text_file.write_text("not a pdf")

    response = upload(text_file)

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Only PDF files are supported."
    )

    assert_no_orphans(storage_dir)
