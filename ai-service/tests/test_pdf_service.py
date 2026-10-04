import pytest

from app.services.pdf_service import extract_pages
from pypdf import PdfWriter


def test_extract_pages_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_pages("does-not-exist.pdf")


def test_extract_pages(tmp_path):
    writer = PdfWriter()

    writer.add_blank_page(width=200, height=200)
    writer.add_blank_page(width=200, height=200)

    pdf_path = tmp_path / "test.pdf"

    with open(pdf_path, "wb") as file:
        writer.write(file)

    pages = extract_pages(pdf_path)

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert pages[1]["page_number"] == 2


def test_extract_pdf_text():
    pdf_path = "tests/fixtures/sample.pdf"

    pages = extract_pages(pdf_path)

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "DocuMind AI" in pages[0]["text"]