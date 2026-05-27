from __future__ import annotations

import pandas as pd


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["ma20"] = result["close"].rolling(window=20, min_periods=1).mean()
    result["ma50"] = result["close"].rolling(window=50, min_periods=1).mean()
    result["ma200"] = result["close"].rolling(window=200, min_periods=1).mean()
    return result
