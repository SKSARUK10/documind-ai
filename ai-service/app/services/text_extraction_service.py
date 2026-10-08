from pathlib import Path

import pandas as pd
from pypdf.errors import PyPdfError

from app.services.document_file_type_service import (
    ALLOWED_FORMATS_MESSAGE,
)
from app.services.pdf_service import extract_pages as extract_pdf_pages


PDF_READ_ERROR_MESSAGE = (
    "The PDF file could not be read. "
    "It may be corrupt or password-protected."
)

CSV_NO_DATA_MESSAGE = (
    "The CSV file does not contain any readable data."
)

CSV_READ_ERROR_MESSAGE = (
    "The CSV file could not be read. "
    "It may be corrupt or use an unsupported encoding."
)

EXCEL_NO_DATA_MESSAGE = (
    "The Excel file does not contain any readable data."
)

EXCEL_READ_ERROR_MESSAGE = (
    "The Excel file could not be read. It may be corrupt."
)


class TextExtractionError(Exception):
    """The uploaded file cannot be converted into readable text."""


def format_cell(value: object) -> str:

    if value is None or pd.isna(value):
        return ""

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def format_rows(frame: pd.DataFrame) -> list[str]:

    columns = [str(column) for column in frame.columns]

    rows = frame.astype(object).to_dict(orient="records")

    return [
        " | ".join(
            f"{column}: {format_cell(row[column])}"
            for column in columns
        )
        for row in rows
    ]


def extract_csv_pages(file_path: Path) -> list[dict]:

    try:
        frame = pd.read_csv(
            file_path,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8-sig",
        )
    except pd.errors.EmptyDataError:
        raise TextExtractionError(CSV_NO_DATA_MESSAGE) from None
    except Exception:
        raise TextExtractionError(CSV_READ_ERROR_MESSAGE) from None

    if frame.empty:
        raise TextExtractionError(CSV_NO_DATA_MESSAGE)

    rows = format_rows(frame)

    text = "\n".join(rows)

    if not text.strip():
        raise TextExtractionError(CSV_NO_DATA_MESSAGE)

    return [
        {
            "page_number": 1,
            "text": text,
        }
    ]


def extract_excel_pages(file_path: Path) -> list[dict]:

    try:
        sheets = pd.read_excel(
            file_path,
            sheet_name=None,
        )
    except Exception:
        raise TextExtractionError(EXCEL_READ_ERROR_MESSAGE) from None

    if not isinstance(sheets, dict):
        sheets = {"Sheet1": sheets}

    pages = []

    for position, (sheet_name, frame) in enumerate(
        sheets.items(),
        start=1,
    ):
        if frame.empty:
            continue

        rows = format_rows(frame)

        text = "\n".join(rows)

        if not text.strip():
            continue

        pages.append(
            {
                "page_number": position,
                "sheet_name": sheet_name or f"Sheet {position}",
                "text": f"Sheet: {sheet_name or f'Sheet {position}'}\n\n{text}",
            }
        )

    if not pages:
        raise TextExtractionError(EXCEL_NO_DATA_MESSAGE)

    return pages


def extract_pages_for_file(
    file_path: Path,
    extension: str,
) -> list[dict]:

    if extension == ".pdf":
        try:
            return extract_pdf_pages(file_path)
        except PyPdfError:
            raise TextExtractionError(PDF_READ_ERROR_MESSAGE) from None

    if extension == ".csv":
        return extract_csv_pages(file_path)

    if extension in {".xlsx", ".xls"}:
        return extract_excel_pages(file_path)

    raise TextExtractionError(ALLOWED_FORMATS_MESSAGE)
