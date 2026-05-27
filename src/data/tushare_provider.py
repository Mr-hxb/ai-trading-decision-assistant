from src.data.base import MarketDataProvider, ProviderError


class TushareProvider(MarketDataProvider):
    def get_daily_bars(self, symbol: str, start_date: str, end_date: str):
        raise ProviderError("TODO: TushareProvider requires TUSHARE_TOKEN from .env and a verified daily/pro_bar mapping.")
