from pathlib import Path

import pandas as pd
import pytest

from app.services.text_extraction_service import (
    CSV_NO_DATA_MESSAGE,
    EXCEL_NO_DATA_MESSAGE,
    TextExtractionError,
    extract_pages_for_file,
)


CSV_CONTENT = (
    "name,department,salary\n"
    "Alice,Engineering,80000\n"
    "Bob,Sales,60000\n"
)


def write_workbook(path, sheets: dict[str, pd.DataFrame]):

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, frame in sheets.items():
            frame.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
            )

    return path


def test_csv_rows_include_column_names(tmp_path):

    csv_path = tmp_path / "employees.csv"
    csv_path.write_text(CSV_CONTENT, encoding="utf-8")

    pages = extract_pages_for_file(csv_path, ".csv")

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1

    text = pages[0]["text"]

    assert (
        "name: Alice | department: Engineering | salary: 80000"
        in text
    )
    assert "name: Bob | department: Sales | salary: 60000" in text


def test_csv_empty_file_returns_safe_error(tmp_path):

    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")

    with pytest.raises(TextExtractionError) as error:
        extract_pages_for_file(csv_path, ".csv")

    assert str(error.value) == CSV_NO_DATA_MESSAGE


def test_csv_headers_without_rows_returns_safe_error(tmp_path):

    csv_path = tmp_path / "headers.csv"
    csv_path.write_text("name,department,salary\n", encoding="utf-8")

    with pytest.raises(TextExtractionError) as error:
        extract_pages_for_file(csv_path, ".csv")

    assert str(error.value) == CSV_NO_DATA_MESSAGE


def test_corrupt_csv_returns_safe_error(tmp_path):

    csv_path = tmp_path / "corrupt.csv"
    csv_path.write_bytes(b"\x80\x81\x82\xff not valid utf-8")

    with pytest.raises(TextExtractionError) as error:
        extract_pages_for_file(csv_path, ".csv")

    assert "could not be read" in str(error.value)


def test_excel_sheets_keep_names_and_headers(tmp_path):

    workbook_path = write_workbook(
        tmp_path / "sales.xlsx",
        {
            "Employees": pd.DataFrame(
                {
                    "name": ["Alice", "Bob"],
                    "department": ["Engineering", "Sales"],
                    "salary": [80000, 60000],
                }
            ),
            "Targets": pd.DataFrame(
                {
                    "region": ["North", "South"],
                    "target": [120000, 95000],
                }
            ),
        },
    )

    pages = extract_pages_for_file(workbook_path, ".xlsx")

    assert len(pages) == 2

    assert pages[0]["page_number"] == 1
    assert pages[0]["sheet_name"] == "Employees"
    assert pages[0]["text"].startswith("Sheet: Employees\n\n")
    assert (
        "name: Alice | department: Engineering | salary: 80000"
        in pages[0]["text"]
    )

    assert pages[1]["page_number"] == 2
    assert pages[1]["sheet_name"] == "Targets"
    assert pages[1]["text"].startswith("Sheet: Targets\n\n")
    assert "region: North | target: 120000" in pages[1]["text"]


def test_excel_empty_workbook_returns_safe_error(tmp_path):

    workbook_path = write_workbook(
        tmp_path / "empty.xlsx",
        {"Sheet1": pd.DataFrame({"column": []})},
    )

    with pytest.raises(TextExtractionError) as error:
        extract_pages_for_file(workbook_path, ".xlsx")

    assert str(error.value) == EXCEL_NO_DATA_MESSAGE


def test_excel_with_one_empty_sheet_uses_remaining_sheets(tmp_path):

    workbook_path = write_workbook(
        tmp_path / "mixed.xlsx",
        {
            "Empty": pd.DataFrame({"column": []}),
            "Employees": pd.DataFrame({"name": ["Alice"]}),
        },
    )

    pages = extract_pages_for_file(workbook_path, ".xlsx")

    assert len(pages) == 1
    assert pages[0]["sheet_name"] == "Employees"


def test_corrupt_excel_returns_safe_error(tmp_path):

    workbook_path = tmp_path / "corrupt.xlsx"
    workbook_path.write_bytes(b"this is not an excel file")

    with pytest.raises(TextExtractionError) as error:
        extract_pages_for_file(workbook_path, ".xlsx")

    assert "could not be read" in str(error.value)


def test_corrupt_xls_returns_safe_error(tmp_path):

    workbook_path = tmp_path / "corrupt.xls"
    workbook_path.write_bytes(b"this is not an excel file")

    with pytest.raises(TextExtractionError) as error:
        extract_pages_for_file(workbook_path, ".xls")

    assert "could not be read" in str(error.value)


def test_pdf_dispatch_keeps_existing_extraction():

    pages = extract_pages_for_file(
        Path("tests/fixtures/sample.pdf"),
        ".pdf",
    )

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "DocuMind AI" in pages[0]["text"]


def test_unknown_extension_is_rejected(tmp_path):

    text_path = tmp_path / "notes.txt"
    text_path.write_text("not supported")

    with pytest.raises(TextExtractionError):
        extract_pages_for_file(text_path, ".txt")
