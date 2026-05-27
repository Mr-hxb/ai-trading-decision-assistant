import pandas as pd

from src.strategy.risk_rules import calculate_risk


def test_stop_loss_and_rr_ratio():
    df = pd.DataFrame([{"close": 10.2, "low": 10.0, "ma20": 9.8}])
    darvas = {"box_high": 10.0, "box_low": 7.0, "box_width": 3.0}
    result = calculate_risk(df, darvas)
    assert result["stop_loss"] == 10.0
    assert result["stop_loss_reason"] == "breakout_bar_low"
    assert result["risk_amount"] > 0
    assert result["rr_ratio"] > 2


def test_risk_not_crash_when_no_valid_reference():
    df = pd.DataFrame([{"close": 10.0, "low": 11.0, "ma20": 12.0}])
    result = calculate_risk(df, {"box_high": None, "box_low": None, "box_width": None})
    assert result["stop_loss"] is None
    assert result["risk_amount"] == 0.0
    assert result["rr_ratio"] == 0.0
