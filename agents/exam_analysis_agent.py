"""Summarize recurring terms in supplied past-paper text."""
from collections import Counter
import re
from modules.llm_client import generate


class ExamAnalysisAgent:
    def run(self, paper_text, textbook_chunks=None):
        response = generate("Analyze this past-paper text. Identify recurring concepts and suggest revision priorities. Do not claim statistical weightage from a single paper.\n\n" + paper_text[:12000])
        if response:
            return response
        words = re.findall(r"[A-Za-z]{5,}", paper_text.lower())
        common = [(w, n) for w, n in Counter(words).most_common(12) if n > 1]
        if not common:
            return "Add text from one or more past papers to analyze recurring concepts."
        return "## Frequently repeated terms\n\n" + "\n".join(f"- **{w.title()}** — {n} mentions" for w, n in common) + "\n\nThis simple count is a revision signal, not a prediction of exam weightage."
