"""Extract page-aware text from PDFs using PyMuPDF."""
from pathlib import Path
import fitz


def load_pdf(path: str | Path) -> list[dict]:
    pages = []
    with fitz.open(path) as pdf:
        for number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append({"text": text, "source": Path(path).name, "page": number})
    if not pages:
        raise ValueError("No selectable text found. Scanned PDFs need OCR before upload.")
    return pages
