"""Small dependency-light lexical retriever with TF-IDF ranking."""
import re
from collections import Counter
import math


class Retriever:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.docs = [self._terms(c["text"]) for c in chunks]
        self.df = Counter(term for doc in self.docs for term in set(doc))

    @staticmethod
    def _terms(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]{2,}", text.lower())

    def search(self, query: str, k: int = 5) -> list[dict]:
        terms = self._terms(query)
        if not terms:
            return []
        scored = []
        n = len(self.docs)
        for chunk, doc in zip(self.chunks, self.docs):
            counts = Counter(doc)
            score = sum(counts[t] * (math.log((n + 1) / (self.df[t] + 1)) + 1) for t in terms)
            if score:
                scored.append((score, chunk))
        return [c for _, c in sorted(scored, key=lambda item: item[0], reverse=True)[:k]]
