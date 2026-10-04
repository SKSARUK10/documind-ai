from pathlib import Path
from pypdf import PdfReader

def extract_pages(pdf_path: str | Path) -> list[dict]:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"Pdf file not found: {path}")

    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page_number": page_number,
            "text": text,
        })

    return pages