from pathlib import Path

from src.data.mock_provider import MockProvider
from src.orchestrator import Orchestrator


def test_orchestrator_generates_daily_report_and_isolates_failed_symbol(tmp_path):
    result = Orchestrator(MockProvider()).run_scan(["AAPL", "FAIL", "NVDA"], "2024-01-01", "2026-05-25")
    assert "AAPL" in result["successful_symbols"]
    assert "NVDA" in result["successful_symbols"]
    assert any(item["symbol"] == "FAIL" for item in result["failed_symbols"])
    assert result["human_gate"]["human_review_required"] is True
    assert Path(result["report_path"]).exists()
    report_text = Path(result["report_path"]).read_text(encoding="utf-8")
    assert "三流派审查" in report_text
    assert "Darvas Box" in report_text


def test_orchestrator_injects_research_context():
    research_contexts = {
        "AAPL": {
            "symbol": "AAPL",
            "market_context": {"market": "us", "summary": "QQQ trend supportive", "risk_appetite": "positive"},
            "sentiment_summary": "Official and mainstream context is constructive.",
            "company_events": [{"title": "event"}],
            "news_items": [{"title": "news", "sentiment": "positive"}],
        }
    }
    result = Orchestrator(MockProvider()).run_scan(["AAPL"], "2024-01-01", "2026-05-25", research_contexts=research_contexts)
    context = result["per_symbol_results"]["AAPL"]
    assert context["market_regime"]["risk_level"] == "supportive"
    assert context["doctrine_reviews"]
    assert any("舆论摘要" in item for review in context["doctrine_reviews"].values() for item in review["evidence"])
