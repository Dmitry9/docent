"""Retrieval layer: the sources the agent is allowed to cite."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Passage:
    """A retrieved chunk of a source document."""

    source: str
    text: str
    score: float


class Retriever(Protocol):
    """Anything that can find passages relevant to a query."""

    def search(self, query: str, *, limit: int = 5) -> list[Passage]: ...


class KeywordRetriever:
    """Naive in-memory keyword match — placeholder until the pgvector backend lands."""

    def __init__(self, corpus: dict[str, str]) -> None:
        self._corpus = corpus

    def search(self, query: str, *, limit: int = 5) -> list[Passage]:
        terms = {t for t in query.lower().split() if len(t) > 2}
        scored: list[Passage] = []
        for source, text in self._corpus.items():
            words = text.lower().split()
            if not words:
                continue
            hits = sum(w in terms for w in words)
            if hits:
                scored.append(Passage(source=source, text=text, score=hits / len(words)))
        return sorted(scored, key=lambda p: p.score, reverse=True)[:limit]
