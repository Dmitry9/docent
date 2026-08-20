from docent.retrieval import KeywordRetriever


def test_ranks_matching_sources_first() -> None:
    retriever = KeywordRetriever(
        {
            "hit": "python agents everywhere in this text",
            "miss": "nothing relevant here at all",
        }
    )
    results = retriever.search("python agents")
    assert [p.source for p in results] == ["hit"]


def test_respects_limit() -> None:
    corpus = {f"doc{i}": "python python python" for i in range(10)}
    assert len(KeywordRetriever(corpus).search("python", limit=3)) == 3
