from __future__ import annotations

import json
import os
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode

import pandas as pd

from src.data.base import MarketDataProvider, ProviderError, normalize_daily_bars


class EodhdProvider(MarketDataProvider):
    def __init__(
        self,
        api_key: str | None = None,
        api_key_env: str = "EODHD_API_KEY",
        base_url: str = "https://eodhd.com/api",
        timeout: float = 15,
    ) -> None:
        self.api_key = api_key
        self.api_key_env = api_key_env
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_daily_bars(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        if self._is_a_share_symbol(symbol):
            raise ProviderError(f"EODHDProvider does not support A-share symbol {symbol}. Use --provider akshare.")

        api_key = self._get_api_key()
        errors: list[str] = []
        for eodhd_symbol in self._candidate_symbols(symbol):
            try:
                raw = self._fetch_eod(eodhd_symbol, api_key, start_date, end_date)
                return self._normalize(raw, symbol)
            except ProviderError as exc:
                errors.append(f"{eodhd_symbol}: {exc}")

        raise ProviderError(f"EODHD failed to fetch {symbol}. Tried {'; '.join(errors)}")

    def _get_api_key(self) -> str:
        api_key = self.api_key or os.getenv(self.api_key_env, "")
        if not api_key:
            raise ProviderError(f"{self.api_key_env} is not set. Add it to .env before using --provider eodhd.")
        return api_key

    def _fetch_eod(self, symbol: str, api_key: str, start_date: str, end_date: str) -> list[dict]:
        query = urlencode(
            {
                "api_token": api_key,
                "from": start_date,
                "to": end_date,
                "period": "d",
                "fmt": "json",
            }
        )
        url = f"{self.base_url}/eod/{quote(symbol, safe='')}?{query}"
        request = urllib_request.Request(url, headers={"User-Agent": "ai-trading-decision-assistant/0.1"})
        try:
            with urllib_request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            summary = self._summarize_body(body, api_key)
            raise ProviderError(f"EODHD HTTP {exc.code} for {symbol}: {summary}") from exc
        except URLError as exc:
            raise ProviderError(f"EODHD network error for {symbol}: {exc.reason}") from exc
        except OSError as exc:
            raise ProviderError(f"EODHD network error for {symbol}: {exc}") from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            summary = self._summarize_body(body, api_key)
            raise ProviderError(f"EODHD returned invalid JSON for {symbol}: {summary}") from exc

        if isinstance(data, dict):
            summary = self._summarize_body(json.dumps(data, ensure_ascii=False), api_key)
            raise ProviderError(f"EODHD returned an error object for {symbol}: {summary}")
        if not isinstance(data, list):
            raise ProviderError(f"EODHD returned unexpected payload type for {symbol}: {type(data).__name__}")
        if not data:
            raise ProviderError(f"EODHD returned no rows for {symbol}")
        return data

    @staticmethod
    def _normalize(raw: list[dict], symbol: str) -> pd.DataFrame:
        df = pd.DataFrame(raw)
        required = {"date", "open", "high", "low", "close", "volume"}
        missing = sorted(required - set(df.columns))
        if missing:
            raise ProviderError(f"EODHD response is missing required columns: {missing}")
        normalized = df[["date", "open", "high", "low", "close", "volume"]].copy()
        normalized["amount"] = None
        normalized["symbol"] = symbol
        normalized["source"] = "eodhd"
        return normalize_daily_bars(normalized, symbol=symbol, source="eodhd")

    @staticmethod
    def _candidate_symbols(symbol: str) -> list[str]:
        normalized = symbol.strip().upper()
        candidates = [normalized]
        if normalized.endswith(".HK"):
            code = normalized.removesuffix(".HK")
            stripped = code.lstrip("0") or "0"
            fallback = f"{stripped}.HK"
            if fallback != normalized:
                candidates.append(fallback)
        return candidates

    @staticmethod
    def _is_a_share_symbol(symbol: str) -> bool:
        normalized = symbol.strip().upper()
        return normalized.endswith((".SH", ".SZ", ".BJ")) or (normalized.isdigit() and len(normalized) == 6)

    @staticmethod
    def _summarize_body(body: str, api_key: str) -> str:
        redacted = body.replace(api_key, "[redacted]")
        compact = " ".join(redacted.split())
        if not compact:
            return "<empty body>"
        return compact[:240]
