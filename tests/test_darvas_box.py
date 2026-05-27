import pandas as pd

from src.indicators.box_detection import detect_darvas_box


def test_darvas_breakout_signal_and_no_lookahead():
    rows = []
    for i in range(40):
        rows.append({"high": 10.0, "low": 9.0, "close": 9.6, "volume_ratio": 1.0})
    rows.append({"high": 100.0, "low": 10.5, "close": 11.0, "volume_ratio": 2.0})
    df = pd.DataFrame(rows)
    result = detect_darvas_box(df, lookback_days=40, max_range_pct=0.15, breakout_volume_ratio=1.5)
    latest = result.iloc[-1]
    assert latest["box_high"] == 10.0
    assert latest["box_high"] != 100.0
    assert bool(latest["breakout_signal"]) is True


def test_box_too_wide_is_not_in_box():
    rows = [{"high": 12.0, "low": 8.0, "close": 9.0, "volume_ratio": 1.0} for _ in range(40)]
    rows.append({"high": 13.0, "low": 9.0, "close": 13.1, "volume_ratio": 2.0})
    result = detect_darvas_box(pd.DataFrame(rows), lookback_days=40, max_range_pct=0.15)
    assert bool(result.iloc[-1]["in_box"]) is False
    assert bool(result.iloc[-1]["breakout_signal"]) is False
