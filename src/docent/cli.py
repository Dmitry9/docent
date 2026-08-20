"""Command-line entry point: `docent "your question"`."""

import sys

from docent.agent import Deps, build_agent
from docent.retrieval import KeywordRetriever

DEMO_CORPUS = {
    "readme": "docent is a guided Q&A agent over a document collection, "
    "built with pydantic-ai and a pluggable retrieval layer.",
}


def main() -> None:
    if len(sys.argv) < 2:
        print('usage: docent "your question"', file=sys.stderr)
        raise SystemExit(2)
    agent = build_agent()
    deps = Deps(retriever=KeywordRetriever(DEMO_CORPUS))
    result = agent.run_sync(" ".join(sys.argv[1:]), deps=deps)
    print(result.output)
