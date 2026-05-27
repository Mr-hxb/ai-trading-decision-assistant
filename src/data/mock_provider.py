from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.data.base import MarketDataProvider, ProviderError, normalize_daily_bars


class MockProvider(MarketDataProvider):
    """Deterministic daily-bar provider used for tests and local demos."""

    def __init__(self, sample_path: str | Path | None = None) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.sample_path = Path(sample_path) if sample_path else self.project_root / "data/sample/sample_daily_bars.csv"

    def get_daily_bars(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        dates = pd.date_range(start=start_date, end=end_date, freq="B")
        if len(dates) < 45:
            dates = pd.date_range(end=end_date, periods=80, freq="B")
        if symbol == "FAIL":
            raise ProviderError("MockProvider intentional failure for symbol FAIL")
        return self._generate_symbol(symbol, dates)

    def _generate_symbol(self, symbol: str, dates: pd.DatetimeIndex) -> pd.DataFrame:
        n = len(dates)
        index = np.arange(n)
        base_start = {"AAPL": 95.0, "TSLA": 210.0, "NVDA": 420.0}.get(symbol, 80.0)
        trend_slope = {"AAPL": 0.11, "TSLA": -0.03, "NVDA": 0.35}.get(symbol, 0.04)
        close = base_start + index * trend_slope + np.sin(index / 5.0) * 1.2
        volume = np.full(n, 1_000_000.0) + (np.sin(index / 7.0) * 80_000)

        if symbol == "AAPL" and n >= 60:
            box_low = close[-42] * 0.98
            box_high = box_low * 1.08
            for offset, day in enumerate(range(n - 41, n - 1)):
                close[day] = box_low + (box_high - box_low) * (0.35 + 0.25 * np.sin(offset))
                volume[day] = 1_050_000 + (offset % 5) * 20_000
            close[-1] = box_high * 1.035
            volume[-1] = 2_650_000
        elif symbol == "TSLA" and n >= 60:
            close[-1] = close[-2] * 0.99
            volume[-1] = 900_000
        elif symbol == "NVDA" and n >= 60:
            close[-1] = close[-2] * 1.015
            volume[-1] = 1_400_000

        open_ = close * (1 + np.sin(index / 9.0) * 0.004)
        high = np.maximum(open_, close) * 1.01
        low = np.minimum(open_, close) * 0.99
        if symbol == "AAPL" and n >= 60:
            # Keep the final low below the breakout price so risk logic has a protective reference.
            low[-1] = close[-1] * 0.975
            high[-1] = close[-1] * 1.01

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "symbol": symbol,
                "open": open_.round(2),
                "high": high.round(2),
                "low": low.round(2),
                "close": close.round(2),
                "volume": volume.round(0).astype(int),
                "amount": np.nan,
                "source": "mock",
            }
        )
        return normalize_daily_bars(df, symbol=symbol, source="mock")
