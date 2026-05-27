from src.research_context import get_research_context, normalize_research_contexts


def test_normalize_research_context_single_symbol():
    contexts = normalize_research_contexts({"symbol": "iren.us", "sentiment_summary": "mixed"})
    assert contexts["IREN.US"]["sentiment_summary"] == "mixed"


def test_normalize_research_context_symbols_map():
    contexts = normalize_research_contexts({"symbols": {"AAPL": {"sentiment_summary": "constructive"}}})
    assert get_research_context(contexts, "AAPL")["sentiment_summary"] == "constructive"


def test_research_context_lookup_matches_without_exchange_suffix():
    contexts = normalize_research_contexts({"symbol": "IREN.US", "sentiment_summary": "mixed"})
    assert get_research_context(contexts, "IREN")["sentiment_summary"] == "mixed"
