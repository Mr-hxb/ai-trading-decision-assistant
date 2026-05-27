from src.subagents.decision_committee_subagent import DecisionCommitteeSubagent


def base_input():
    return {
        "symbol": "AAPL",
        "config": {"risk": {"min_rr_ratio": 2.0}, "decision_committee": {"require_human_review": True}},
        "pattern_result": {"darvas_box": {"chase_risk": False, "breakout_signal": True}},
        "trend_result": {"trend_ok": True},
        "risk_result": {"stop_loss": 10.0, "rr_ratio": 3.0, "risk_flags": []},
        "discipline_result": {"discipline_flags": [], "fomo_risk": False},
        "bearish_evidence": [],
        "bullish_evidence": ["结构证据"],
        "serious_risk": False,
        "score_result": {"score": 90},
    }


def run_committee(data):
    return DecisionCommitteeSubagent().run(data).data["decision_result"]


def test_chase_risk_cannot_be_top_status():
    data = base_input()
    data["pattern_result"]["darvas_box"]["chase_risk"] = True
    decision = run_committee(data)
    assert decision["decision_status"] != "可关注"


def test_low_rr_cannot_be_top_status():
    data = base_input()
    data["risk_result"]["rr_ratio"] = 1.0
    decision = run_committee(data)
    assert decision["decision_status"] != "可关注"


def test_bad_trend_cannot_be_top_status():
    data = base_input()
    data["trend_result"]["trend_ok"] = False
    decision = run_committee(data)
    assert decision["decision_status"] != "可关注"


def test_doctrine_reject_downgrades_top_status():
    data = base_input()
    data["doctrine_reviews"] = {
        "DarvasDoctrineSubagent": {"name": "Darvas Box", "verdict": "reject"},
    }
    decision = run_committee(data)
    assert decision["decision_status"] == "观察"
    assert "Darvas Box" in decision["why_not_higher_status"]


def test_output_has_no_forbidden_trade_words_and_requires_human_review():
    decision = run_committee(base_input())
    as_text = str(decision)
    assert "买入" not in as_text
    assert "卖出" not in as_text
    assert decision["human_review_required"] is True
