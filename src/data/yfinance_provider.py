from src.data.base import MarketDataProvider, ProviderError


class YfinanceProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: YfinanceProvider will normalize yfinance.download output when enabled.")
