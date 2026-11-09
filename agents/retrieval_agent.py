"""Find textbook passages relevant to a student query."""
from modules.retriever import Retriever


class RetrievalAgent:
    def __init__(self, chunks):
        self.index = Retriever(chunks)

    def retrieve(self, query, k=5):
        return self.index.search(query, k)
