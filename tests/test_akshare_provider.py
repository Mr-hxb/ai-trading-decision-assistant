import sys

import pandas as pd

from src.data.akshare_provider import AkshareProvider
from src.orchestrator import build_provider


class FakeAkshare:
    def __init__(self):
        self.calls = []
        self.fail_hist = False
        self.fail_hk_hist = False

    def stock_zh_a_hist(self, **kwargs):
        self.calls.append(("cn", kwargs))
        if self.fail_hist:
            raise RuntimeError("hist unavailable")
        return pd.DataFrame(
            [
                {
                    "日期": "2024-01-02",
                    "开盘": 10.0,
                    "最高": 11.0,
                    "最低": 9.8,
                    "收盘": 10.5,
                    "成交量": 1234,
                    "成交额": 123456.0,
                }
            ]
        )

    def stock_hk_hist(self, **kwargs):
        self.calls.append(("hk", kwargs))
        if self.fail_hk_hist:
            raise RuntimeError("hk hist unavailable")
        return pd.DataFrame(
            [
                {
                    "日期": "2024-01-02",
                    "开盘": 300.0,
                    "最高": 310.0,
                    "最低": 295.0,
                    "收盘": 305.0,
                    "成交量": 2000000,
                    "成交额": 600000000.0,
                }
            ]
        )

    def stock_hk_daily(self, **kwargs):
        self.calls.append(("hk_daily", kwargs))
        return pd.DataFrame(
            [
                {
                    "date": "2023-12-29",
                    "open": 290.0,
                    "high": 295.0,
                    "low": 285.0,
                    "close": 292.0,
                    "volume": 1000000,
                    "amount": 292000000.0,
                },
                {
                    "date": "2024-01-02",
                    "open": 300.0,
                    "high": 310.0,
                    "low": 295.0,
                    "close": 305.0,
                    "volume": 2000000,
                    "amount": 600000000.0,
                },
            ]
        )

    def stock_us_hist(self, **kwargs):
        self.calls.append(("us", kwargs))
        return pd.DataFrame(
            [
                {
                    "日期": "2024-01-02",
                    "开盘": 100.0,
                    "最高": 102.0,
                    "最低": 99.0,
                    "收盘": 101.0,
                    "成交量": 3000000,
                    "成交额": 303000000.0,
                }
            ]
        )

    def stock_zh_a_daily(self, **kwargs):
        self.calls.append(("cn_daily", kwargs))
        return pd.DataFrame(
            [
                {
                    "date": "2024-01-02",
                    "open": 10.0,
                    "high": 11.0,
                    "low": 9.8,
                    "close": 10.5,
                    "volume": 123400,
                    "amount": 123456.0,
                }
            ]
        )


def test_akshare_cn_symbol_normalization_and_volume_unit(monkeypatch):
    fake = FakeAkshare()
    monkeypatch.setitem(sys.modules, "akshare", fake)
    result = AkshareProvider(adjust="qfq").get_daily_bars("000001.SZ", "2024-01-01", "2024-01-31")
    assert fake.calls[0][0] == "cn"
    assert fake.calls[0][1]["symbol"] == "000001"
    assert fake.calls[0][1]["adjust"] == "qfq"
    assert result.iloc[0]["volume"] == 123400
    assert result.iloc[0]["source"] == "akshare:cn:qfq"


def test_akshare_cn_daily_fallback(monkeypatch):
    fake = FakeAkshare()
    fake.fail_hist = True
    monkeypatch.setitem(sys.modules, "akshare", fake)
    result = AkshareProvider(adjust="qfq").get_daily_bars("002475.SZ", "2024-01-01", "2024-01-31")
    assert fake.calls[0][0] == "cn"
    assert fake.calls[1] == (
        "cn_daily",
        {"symbol": "sz002475", "start_date": "20240101", "end_date": "20240131", "adjust": "qfq"},
    )
    assert result.iloc[0]["volume"] == 123400


def test_akshare_hk_daily_fallback(monkeypatch):
    fake = FakeAkshare()
    fake.fail_hk_hist = True
    monkeypatch.setitem(sys.modules, "akshare", fake)
    result = AkshareProvider(adjust="qfq").get_daily_bars("09868.HK", "2024-01-01", "2024-01-31")
    assert fake.calls[0][0] == "hk"
    assert fake.calls[1] == ("hk_daily", {"symbol": "09868", "adjust": "qfq"})
    assert len(result) == 1
    assert str(result.iloc[0]["date"])[:10] == "2024-01-02"
    assert result.iloc[0]["source"] == "akshare:hk:qfq"


def test_akshare_hk_and_us_routing(monkeypatch):
    fake = FakeAkshare()
    monkeypatch.setitem(sys.modules, "akshare", fake)
    provider = AkshareProvider(adjust="")
    hk = provider.get_daily_bars("700.HK", "2024-01-01", "2024-01-31")
    us = provider.get_daily_bars("106.TTE", "2024-01-01", "2024-01-31")
    assert fake.calls[0] == (
        "hk",
        {"symbol": "00700", "period": "daily", "start_date": "20240101", "end_date": "20240131", "adjust": ""},
    )
    assert fake.calls[1][0] == "us"
    assert fake.calls[1][1]["symbol"] == "106.TTE"
    assert hk.iloc[0]["source"] == "akshare:hk:none"
    assert us.iloc[0]["source"] == "akshare:us:none"


def test_build_provider_accepts_akshare_adjust():
    provider = build_provider("akshare", adjust="hfq")
    assert isinstance(provider, AkshareProvider)
    assert provider.adjust == "hfq"
