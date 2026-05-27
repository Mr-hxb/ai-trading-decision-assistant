from src.data.base import MarketDataProvider, ProviderError


class PolygonProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: PolygonProvider requires POLYGON_API_KEY from .env.")
