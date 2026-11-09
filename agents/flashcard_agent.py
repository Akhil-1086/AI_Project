"""Create active-recall cards from retrieved textbook context."""
import re
from modules.llm_client import generate


class FlashcardAgent:
    def run(self, topic, passages):
        context = "\n".join(p["text"] for p in passages)
        answer = generate(f"Make 5 concise question/answer flashcards about {topic} using only this context. Return one per line as Q: ... | A: ...\n{context}")
        if answer:
            cards = []
            for line in answer.splitlines():
                match = re.match(r"\s*Q:\s*(.*?)\s*\|\s*A:\s*(.*)", line)
                if match:
                    cards.append({"question": match.group(1), "answer": match.group(2), "source": "Generated from retrieved passages"})
            if cards:
                return cards
        cards = []
        for p in passages[:5]:
            sentence = re.split(r"(?<=[.!?])\s+", p["text"])[0].strip()
            if len(sentence) > 25:
                cards.append({"question": f"What does the textbook explain about {topic}?", "answer": sentence, "source": f"{p['source']}, page {p['page']}"})
        return cards
