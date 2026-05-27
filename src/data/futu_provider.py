from src.data.base import MarketDataProvider, ProviderError


class FutuProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: FutuProvider will use quote history only; no trading execution API is implemented.")
