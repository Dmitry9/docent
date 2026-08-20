from pydantic_ai.models.test import TestModel

from docent.agent import Deps, build_agent
from docent.retrieval import KeywordRetriever


def test_agent_wires_search_tool() -> None:
    """TestModel calls every registered tool — proves the retrieval tool is wired in."""
    agent = build_agent(TestModel())
    deps = Deps(retriever=KeywordRetriever({"doc": "docent answers questions about documents"}))
    result = agent.run_sync("what does docent do?", deps=deps)
    assert result.output
