from src.data.base import MarketDataProvider, ProviderError


class TiingoProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: TiingoProvider requires TIINGO_API_KEY from .env.")
