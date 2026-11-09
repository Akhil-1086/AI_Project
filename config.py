"""Application settings loaded from environment variables."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
BOOKS_DIR = ROOT / "data" / "books"
OUTPUTS_DIR = ROOT / "outputs"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
CHUNK_SIZE = 900
CHUNK_OVERLAP = 140
TOP_K = 5
