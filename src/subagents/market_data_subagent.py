from __future__ import annotations

from src.data.base import MarketDataProvider, ProviderError
from src.subagents.base import BaseSubagent, SubagentResult


class MarketDataSubagent(BaseSubagent):
    name = "MarketDataSubagent"

    def __init__(self, provider: MarketDataProvider) -> None:
        self.provider = provider

    def run(self, input_data):
        symbol = input_data["symbol"]
        try:
            bars = self.provider.get_daily_bars(symbol, input_data["start_date"], input_data["end_date"])
        except ProviderError as exc:
            return SubagentResult(self.name, "failed", errors=[str(exc)])
        warnings = []
        if bars.empty:
            return SubagentResult(self.name, "failed", errors=[f"No daily bars returned for {symbol}"])
        if bars.isna().any().any():
            warnings.append("Daily bars contain missing values; amount may be unavailable for some providers.")
        return SubagentResult(self.name, "success", {"bars": bars, "row_count": len(bars), "symbol": symbol}, warnings=warnings)
