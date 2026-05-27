from src.data.base import MarketDataProvider, ProviderError


class LongbridgeProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: LongbridgeProvider will use quote history candlesticks only; credentials must come from .env.")
