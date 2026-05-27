from __future__ import annotations

import numpy as np
import pandas as pd


def add_volume_indicators(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["volume_ma20"] = result["volume"].rolling(window=20, min_periods=1).mean()
    denominator = result["volume_ma20"].replace(0, np.nan)
    result["volume_ratio"] = result["volume"] / denominator
    result["volume_ratio"] = result["volume_ratio"].replace([np.inf, -np.inf], np.nan)
    return result
