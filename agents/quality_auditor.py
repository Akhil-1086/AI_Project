"""Check that generated materials include source grounding and useful content."""
from modules.llm_client import generate


class QualityAuditor:
    def review(self, content, passages):
        if not content.strip():
            return {"status": "Needs improvement", "notes": "No content was generated."}
        if not passages:
            return {"status": "Needs review", "notes": "No source passages were retrieved; verify every claim."}
        cited_pages = {p["page"] for p in passages}
        response = generate("Review these study notes only for whether they stay within the supplied textbook excerpts. Reply with grounded / review and one brief reason.\nNOTES:\n" + content[:5000] + "\nSOURCES:\n" + "\n".join(p["text"][:700] for p in passages[:4]))
        if response:
            return {"status": "AI review", "notes": response}
        return {"status": "Source-backed", "notes": f"Generated using retrieved textbook passages from page(s): {', '.join(map(str, sorted(cited_pages)))}. This is a citation check, not a guarantee of correctness."}
