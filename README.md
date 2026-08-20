# docent

A guided Q&A agent over a document collection: a [pydantic-ai](https://ai.pydantic.dev)
agent that must search before it answers, and cite what it found.

> **Status: early scaffold.** Agent wiring, a pluggable retrieval interface, and
> quality gates are in place. The current retriever is a naive keyword matcher over
> an in-memory corpus; a pgvector-backed retriever and an eval harness are next.
> Not production software.

## How it works

The agent (`src/docent/agent.py`) is built by `build_agent(model)` — the model is
injected so tests can substitute a fake. Its system prompt enforces one behavior:
call the `search` tool first, answer only from the returned passages, cite sources.

`search` delegates to a `Retriever` — a structural interface (`typing.Protocol`) in
`src/docent/retrieval.py`. Any object with a matching `search(query, *, limit=5)`
method satisfies it; `KeywordRetriever` is the current in-memory implementation.

## Usage

Requires Python 3.13+, [uv](https://docs.astral.sh/uv/), and an `ANTHROPIC_API_KEY`
in the environment:

```bash
uv run docent "what is docent?"
```

The demo corpus is one hard-coded paragraph (see `cli.py`); the point of the CLI is
wiring, not content.

## Development

```bash
uv sync                       # venv + all deps
uv run ruff format --check .  # formatting
uv run ruff check .           # lint
uv run pyright                # strict type-check
uv run pytest --cov           # tests + coverage
```

All gates must pass. Tests are offline: pydantic-ai's `TestModel` fakes the LLM, so
no API key and no cost. Real-LLM tests carry the `llm` marker and are excluded by
default; run them with `uv run pytest -m llm`.

## Layout

```
src/docent/
  agent.py      build_agent(), Deps, system prompt
  retrieval.py  Passage, Retriever, KeywordRetriever
  cli.py        console-script entry point
tests/
```

## Roadmap

- [ ] pgvector retriever (Postgres + embeddings) replacing the keyword placeholder
- [x] GitHub Actions CI running the gates above
- [ ] eval harness for answer quality (pydantic_evals / LLM-as-judge)
