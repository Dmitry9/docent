"""docent — a guided Q&A agent over a document collection."""

from docent.agent import Deps, build_agent
from docent.retrieval import Passage, Retriever

__all__ = ["Deps", "Passage", "Retriever", "build_agent"]
