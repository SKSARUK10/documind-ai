import pytest

from app.services.document_file_type_service import (
    ALLOWED_FORMATS_MESSAGE,
    UnsupportedFileTypeError,
    resolve_supported_extension,
)


def test_supported_extensions_resolve():

    assert (
        resolve_supported_extension("report.pdf", "application/pdf")
        == ".pdf"
    )
    assert (
        resolve_supported_extension("employees.csv", "text/csv")
        == ".csv"
    )
    assert (
        resolve_supported_extension(
            "sales.xlsx",
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet",
        )
        == ".xlsx"
    )
    assert (
        resolve_supported_extension(
            "legacy-data.xls",
            "application/vnd.ms-excel",
        )
        == ".xls"
    )


def test_extension_is_case_insensitive():

    assert (
        resolve_supported_extension("REPORT.PDF", "application/pdf")
        == ".pdf"
    )


def test_unsupported_extension_is_rejected():

    with pytest.raises(UnsupportedFileTypeError) as error:
        resolve_supported_extension("notes.txt", "text/plain")

    assert str(error.value) == ALLOWED_FORMATS_MESSAGE


def test_mismatched_mime_is_rejected():

    with pytest.raises(UnsupportedFileTypeError):
        resolve_supported_extension("report.pdf", "text/plain")

    with pytest.raises(UnsupportedFileTypeError):
        resolve_supported_extension("employees.csv", "application/pdf")


def test_missing_content_type_is_rejected():

    with pytest.raises(UnsupportedFileTypeError):
        resolve_supported_extension("employees.csv", None)


def test_missing_filename_is_rejected():

    with pytest.raises(UnsupportedFileTypeError):
        resolve_supported_extension(None, "application/pdf")
