"""Split page text into overlapping chunks while keeping citations."""
from config import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_pages(pages: list[dict], size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    chunks = []
    step = max(1, size - overlap)
    for page in pages:
        text = page["text"]
        for start in range(0, len(text), step):
            piece = text[start:start + size].strip()
            if piece:
                chunks.append({**page, "text": piece, "chunk": len(chunks) + 1})
            if start + size >= len(text):
                break
    return chunks
