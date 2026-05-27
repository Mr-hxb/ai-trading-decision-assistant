from __future__ import annotations

import pandas as pd


def relative_strength(stock_df: pd.DataFrame, index_df: pd.DataFrame, days: int = 20) -> float | None:
    if len(stock_df) < 2 or len(index_df) < 2:
        return None
    stock_window = stock_df.tail(days + 1)
    index_window = index_df.tail(days + 1)
    if len(stock_window) < 2 or len(index_window) < 2:
        return None
    stock_return = stock_window["close"].iloc[-1] / stock_window["close"].iloc[0] - 1
    index_return = index_window["close"].iloc[-1] / index_window["close"].iloc[0] - 1
    return float(stock_return - index_return)
