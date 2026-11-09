"""Export generated notes as Markdown."""
from pathlib import Path
from datetime import datetime


def save_markdown(title: str, content: str, folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    safe = "".join(c.lower() if c.isalnum() else "-" for c in title).strip("-")[:60] or "study-notes"
    path = folder / f"{safe}-{datetime.now():%Y%m%d-%H%M%S}.md"
    path.write_text(f"# {title}\n\n{content}\n", encoding="utf-8")
    return path
