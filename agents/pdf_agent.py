"""PDF ingestion agent."""
from modules.pdf_loader import load_pdf
from modules.chunker import chunk_pages


class PDFAgent:
    def process(self, path):
        pages = load_pdf(path)
        return chunk_pages(pages), len(pages)
