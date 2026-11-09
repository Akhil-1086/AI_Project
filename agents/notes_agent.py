"""Generate grounded revision notes from retrieved passages."""
from modules.llm_client import generate


class NotesAgent:
    def run(self, topic, passages):
        context = "\n\n".join(f"[{p['source']}, p.{p['page']}] {p['text']}" for p in passages)
        answer = generate(f"Create clear revision notes about: {topic}. Use headings and bullets. Only use this textbook context and state if it is insufficient.\n\n{context}")
        if answer:
            return answer
        if not passages:
            return "No relevant passages were found. Try a more specific topic or upload a textbook."
        return "## Key points\n\n" + "\n\n".join(f"- **Textbook, page {p['page']}:** {p['text']}" for p in passages)
