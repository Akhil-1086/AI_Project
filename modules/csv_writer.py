"""Export flashcards as a spreadsheet-friendly CSV."""
import csv
from pathlib import Path


def to_csv(cards: list[dict]) -> str:
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["question", "answer", "source"])
    writer.writeheader()
    writer.writerows(cards)
    return output.getvalue()


def save_csv(cards: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_csv(cards), encoding="utf-8-sig")
    return path
