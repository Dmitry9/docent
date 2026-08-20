"""The docent agent: answers questions using only retrieved passages."""

from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model

from docent.retrieval import Passage, Retriever

SYSTEM_PROMPT = (
    "You are a docent: you answer questions about a document collection. "
    "Always call the search tool first and answer only from the passages it returns, "
    "citing the source of each claim. If the passages don't contain the answer, say so."
)


@dataclass
class Deps:
    """Dependencies injected into every agent run."""

    retriever: Retriever


def build_agent(model: Model | str = "anthropic:claude-sonnet-5") -> Agent[Deps, str]:
    agent: Agent[Deps, str] = Agent(model, deps_type=Deps, system_prompt=SYSTEM_PROMPT)

    @agent.tool
    def search(ctx: RunContext[Deps], query: str) -> list[Passage]:  # pyright: ignore[reportUnusedFunction]
        """Find passages in the collection relevant to the query."""
        return ctx.deps.retriever.search(query)

    return agent
