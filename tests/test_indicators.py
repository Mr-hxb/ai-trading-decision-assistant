import numpy as np
import pandas as pd

from src.indicators.moving_average import add_moving_averages
from src.indicators.volume import add_volume_indicators


def test_moving_averages_and_volume_ratio():
    df = pd.DataFrame({"close": np.arange(1, 61, dtype=float), "volume": [100.0] * 60})
    result = add_volume_indicators(add_moving_averages(df))
    assert result["ma20"].iloc[-1] == sum(range(41, 61)) / 20
    assert result["ma50"].iloc[-1] == sum(range(11, 61)) / 50
    assert result["volume_ma20"].iloc[-1] == 100.0
    assert result["volume_ratio"].iloc[-1] == 1.0


def test_volume_ratio_safe_when_volume_ma_is_zero():
    df = pd.DataFrame({"close": [1, 2, 3], "volume": [0, 0, 0]})
    result = add_volume_indicators(df)
    assert result["volume_ratio"].isna().all()
