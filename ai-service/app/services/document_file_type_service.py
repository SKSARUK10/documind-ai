from pathlib import Path


ALLOWED_FORMATS_MESSAGE = (
    "Only PDF, CSV, XLSX, and XLS files are allowed."
)


SUPPORTED_TYPES: dict[str, set[str]] = {
    ".pdf": {
        "application/pdf",
    },
    ".csv": {
        "text/csv",
        "application/csv",
        "text/comma-separated-values",
        "application/vnd.ms-excel",
    },
    ".xlsx": {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
    ".xls": {
        "application/vnd.ms-excel",
    },
}


class UnsupportedFileTypeError(Exception):
    """The uploaded file extension or MIME type is not supported."""


def resolve_supported_extension(
    filename: str | None,
    content_type: str | None,
) -> str:

    extension = Path(filename or "").suffix.lower()

    allowed_content_types = SUPPORTED_TYPES.get(extension)

    if allowed_content_types is None:
        raise UnsupportedFileTypeError(ALLOWED_FORMATS_MESSAGE)

    media_type = (
        (content_type or "")
        .partition(";")[0]
        .strip()
        .lower()
    )

    if media_type not in allowed_content_types:
        raise UnsupportedFileTypeError(ALLOWED_FORMATS_MESSAGE)

    return extension
