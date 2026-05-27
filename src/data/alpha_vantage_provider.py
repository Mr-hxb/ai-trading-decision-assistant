from src.data.base import MarketDataProvider, ProviderError


class AlphaVantageProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: AlphaVantageProvider requires ALPHA_VANTAGE_API_KEY from .env.")
