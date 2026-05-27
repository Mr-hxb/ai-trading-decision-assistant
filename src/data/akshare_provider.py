from __future__ import annotations

import re

import pandas as pd

from src.data.base import MarketDataProvider, ProviderError, normalize_daily_bars


class AkshareProvider(MarketDataProvider):
    def __init__(self, adjust: str = "qfq", timeout: float | None = None) -> None:
        self.adjust = adjust
        self.timeout = timeout

    def get_daily_bars(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            import akshare as ak  # type: ignore
        except ImportError as exc:
            raise ProviderError(
                "akshare is not installed. Run `pip install akshare` or `pip install -r requirements-akshare.txt` "
                "before using --provider akshare."
            ) from exc

        start = start_date.replace("-", "")
        end = end_date.replace("-", "")
        market = self._detect_market(symbol)
        raw_symbol = self._to_akshare_symbol(symbol, market)
        try:
            raw = self._fetch(ak, market, raw_symbol, start, end)
        except Exception as exc:  # pragma: no cover - depends on network/provider availability
            raise ProviderError(f"AKShare failed to fetch {symbol} as {market} symbol {raw_symbol}: {exc}") from exc

        if raw.empty:
            raise ProviderError(f"AKShare returned no rows for {symbol} as {market} symbol {raw_symbol}")

        renamed = self._rename_columns(raw)
        if market == "cn" and raw.attrs.get("volume_unit") == "lots":
            # AKShare stock_zh_a_hist returns A-share volume in lots. Convert lots to shares.
            renamed["volume"] = pd.to_numeric(renamed["volume"], errors="coerce") * 100
        renamed["symbol"] = symbol
        renamed["source"] = f"akshare:{market}:{self.adjust or 'none'}"
        return normalize_daily_bars(renamed, symbol=symbol, source=renamed["source"].iloc[0])

    def _fetch(self, ak, market: str, raw_symbol: str, start: str, end: str) -> pd.DataFrame:
        kwargs = {
            "symbol": raw_symbol,
            "period": "daily",
            "start_date": start,
            "end_date": end,
            "adjust": self.adjust,
        }
        if self.timeout is not None:
            kwargs["timeout"] = self.timeout
        if market == "cn":
            try:
                raw = ak.stock_zh_a_hist(**kwargs)
                raw.attrs["volume_unit"] = "lots"
                return raw
            except Exception as hist_exc:
                daily_symbol = self._to_akshare_daily_symbol(raw_symbol)
                daily_kwargs = {
                    "symbol": daily_symbol,
                    "start_date": start,
                    "end_date": end,
                    "adjust": self.adjust,
                }
                if self.timeout is not None:
                    daily_kwargs["timeout"] = self.timeout
                try:
                    raw = ak.stock_zh_a_daily(**daily_kwargs)
                    raw.attrs["volume_unit"] = "shares"
                    return raw
                except Exception as daily_exc:
                    raise ProviderError(
                        f"stock_zh_a_hist failed: {hist_exc}; stock_zh_a_daily fallback failed: {daily_exc}"
                    ) from daily_exc
        if market == "hk":
            try:
                return ak.stock_hk_hist(**kwargs)
            except Exception as hist_exc:
                try:
                    raw = ak.stock_hk_daily(symbol=raw_symbol, adjust=self.adjust)
                    return self._filter_by_date(raw, start, end)
                except Exception as daily_exc:
                    raise ProviderError(
                        f"stock_hk_hist failed: {hist_exc}; stock_hk_daily fallback failed: {daily_exc}"
                    ) from daily_exc
        if market == "us":
            return ak.stock_us_hist(**kwargs)
        raise ProviderError(f"Unsupported AKShare market: {market}")

    @staticmethod
    def _filter_by_date(raw: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
        date_col = "date" if "date" in raw.columns else "日期" if "日期" in raw.columns else None
        if date_col is None:
            return raw
        filtered = raw.copy()
        dates = pd.to_datetime(filtered[date_col], errors="coerce").dt.strftime("%Y%m%d")
        return filtered[(dates >= start) & (dates <= end)]

    @staticmethod
    def _detect_market(symbol: str) -> str:
        normalized = symbol.strip().upper()
        if normalized.endswith((".SH", ".SZ", ".BJ")) or re.fullmatch(r"\d{6}", normalized):
            return "cn"
        if normalized.endswith(".HK") or re.fullmatch(r"\d{5}", normalized):
            return "hk"
        if re.fullmatch(r"(\d+\.)?[A-Z][A-Z0-9.-]{0,12}", normalized):
            return "us"
        raise ProviderError(
            f"Cannot infer AKShare market from symbol {symbol}. Use examples like 600519.SH, 000001.SZ, 00700.HK, or AKShare US codes such as 106.TTE."
        )

    @staticmethod
    def _to_akshare_symbol(symbol: str, market: str) -> str:
        normalized = symbol.strip().upper()
        if market == "cn":
            return normalized.split(".")[0]
        if market == "hk":
            return normalized.removesuffix(".HK").zfill(5)
        return normalized

    @staticmethod
    def _to_akshare_daily_symbol(raw_symbol: str) -> str:
        if raw_symbol.startswith(("6", "9")):
            return f"sh{raw_symbol}"
        if raw_symbol.startswith(("0", "2", "3")):
            return f"sz{raw_symbol}"
        if raw_symbol.startswith(("4", "8")):
            return f"bj{raw_symbol}"
        raise ProviderError(f"Cannot infer stock_zh_a_daily exchange prefix for raw symbol {raw_symbol}")

    @staticmethod
    def _rename_columns(raw: pd.DataFrame) -> pd.DataFrame:
        renamed = raw.rename(
            columns={
                "日期": "date",
                "date": "date",
                "开盘": "open",
                "open": "open",
                "最高": "high",
                "high": "high",
                "最低": "low",
                "low": "low",
                "收盘": "close",
                "close": "close",
                "成交量": "volume",
                "volume": "volume",
                "成交额": "amount",
                "amount": "amount",
            }
        )
        required = {"date", "open", "high", "low", "close", "volume"}
        missing = sorted(required - set(renamed.columns))
        if missing:
            raise ProviderError(f"AKShare response is missing required columns after normalization: {missing}")
        if "amount" not in renamed:
            renamed["amount"] = None
        return renamed
