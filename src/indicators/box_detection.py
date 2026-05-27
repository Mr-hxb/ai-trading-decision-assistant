from __future__ import annotations

import pandas as pd


def detect_darvas_box(
    df: pd.DataFrame,
    lookback_days: int = 40,
    max_range_pct: float = 0.15,
    breakout_volume_ratio: float = 1.5,
) -> pd.DataFrame:
    result = df.copy()
    rolling_high = result["high"].rolling(window=lookback_days, min_periods=lookback_days).max().shift(1)
    rolling_low = result["low"].rolling(window=lookback_days, min_periods=lookback_days).min().shift(1)
    result["box_high"] = rolling_high
    result["box_low"] = rolling_low
    result["box_width"] = result["box_high"] - result["box_low"]
    result["box_range_pct"] = result["box_width"] / result["box_low"]
    result["in_box"] = result["box_range_pct"].le(max_range_pct).fillna(False)
    result["breakout_signal"] = (
        result["in_box"]
        & result["box_high"].notna()
        & result["close"].gt(result["box_high"])
        & result.get("volume_ratio", pd.Series(index=result.index, dtype=float)).gt(breakout_volume_ratio)
    )
    return result
