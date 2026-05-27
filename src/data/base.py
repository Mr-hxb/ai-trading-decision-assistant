from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = ["date", "symbol", "open", "high", "low", "close", "volume", "amount", "source"]


class ProviderError(RuntimeError):
    """Raised when a market data provider cannot return normalized daily bars."""


class MarketDataProvider(ABC):
    @abstractmethod
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Return daily bars with normalized columns."""


def normalize_daily_bars(df: pd.DataFrame, symbol: str, source: str) -> pd.DataFrame:
    normalized = df.copy()
    if "amount" not in normalized:
        normalized["amount"] = None
    normalized["symbol"] = normalized.get("symbol", symbol)
    normalized["source"] = normalized.get("source", source)
    normalized["date"] = pd.to_datetime(normalized["date"]).dt.strftime("%Y-%m-%d")
    for column in ["open", "high", "low", "close", "volume"]:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")
    if "amount" in normalized:
        normalized["amount"] = pd.to_numeric(normalized["amount"], errors="coerce")
    normalized = normalized[REQUIRED_COLUMNS].sort_values("date").reset_index(drop=True)
    return normalized


def validate_columns(columns: Iterable[str]) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing:
        raise ProviderError(f"Missing normalized daily bar columns: {missing}")
