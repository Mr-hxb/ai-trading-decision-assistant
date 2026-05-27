from __future__ import annotations

import io
import json
from urllib.error import HTTPError

import pytest

from src.data.base import ProviderError
from src.data.eodhd_provider import EodhdProvider
from src.orchestrator import build_provider


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_eodhd_provider_normalizes_daily_bars(monkeypatch):
    calls = []

    def fake_urlopen(request, timeout):
        calls.append((request.full_url, timeout))
        return FakeResponse(
            [
                {
                    "date": "2024-01-02",
                    "open": 10.0,
                    "high": 11.0,
                    "low": 9.5,
                    "close": 10.5,
                    "adjusted_close": 10.4,
                    "volume": 123456,
                }
            ]
        )

    monkeypatch.setattr("src.data.eodhd_provider.urllib_request.urlopen", fake_urlopen)
    result = EodhdProvider(api_key="test-key").get_daily_bars("AAPL.US", "2024-01-01", "2024-01-31")

    assert calls[0][1] == 15
    assert "/eod/AAPL.US?" in calls[0][0]
    assert result.columns.tolist() == ["date", "symbol", "open", "high", "low", "close", "volume", "amount", "source"]
    assert result.iloc[0]["symbol"] == "AAPL.US"
    assert result.iloc[0]["close"] == 10.5
    assert result.iloc[0]["source"] == "eodhd"


def test_eodhd_provider_hk_symbol_fallback_strips_leading_zero(monkeypatch):
    calls = []

    def fake_urlopen(request, timeout):
        calls.append(request.full_url)
        if "/eod/09868.HK?" in request.full_url:
            return FakeResponse([])
        return FakeResponse(
            [
                {
                    "date": "2024-01-02",
                    "open": 60.0,
                    "high": 62.0,
                    "low": 59.0,
                    "close": 61.0,
                    "volume": 2000000,
                }
            ]
        )

    monkeypatch.setattr("src.data.eodhd_provider.urllib_request.urlopen", fake_urlopen)
    result = EodhdProvider(api_key="test-key").get_daily_bars("09868.HK", "2024-01-01", "2024-01-31")

    assert "/eod/09868.HK?" in calls[0]
    assert "/eod/9868.HK?" in calls[1]
    assert result.iloc[0]["symbol"] == "09868.HK"
    assert result.iloc[0]["source"] == "eodhd"


def test_eodhd_provider_requires_api_key(monkeypatch):
    monkeypatch.delenv("EODHD_API_KEY", raising=False)
    with pytest.raises(ProviderError, match="EODHD_API_KEY is not set"):
        EodhdProvider().get_daily_bars("AAPL.US", "2024-01-01", "2024-01-31")


@pytest.mark.parametrize("status_code", [401, 403, 429, 500])
def test_eodhd_provider_http_errors_are_readable_and_redacted(monkeypatch, status_code):
    def fake_urlopen(request, timeout):
        body = io.BytesIO(b'{"message":"bad token secret-token"}')
        raise HTTPError(request.full_url, status_code, "error", hdrs=None, fp=body)

    monkeypatch.setattr("src.data.eodhd_provider.urllib_request.urlopen", fake_urlopen)
    with pytest.raises(ProviderError) as exc_info:
        EodhdProvider(api_key="secret-token").get_daily_bars("AAPL.US", "2024-01-01", "2024-01-31")

    message = str(exc_info.value)
    assert f"HTTP {status_code}" in message
    assert "secret-token" not in message
    assert "[redacted]" in message


def test_eodhd_provider_rejects_empty_payload(monkeypatch):
    monkeypatch.setattr("src.data.eodhd_provider.urllib_request.urlopen", lambda request, timeout: FakeResponse([]))
    with pytest.raises(ProviderError, match="returned no rows"):
        EodhdProvider(api_key="test-key").get_daily_bars("AAPL.US", "2024-01-01", "2024-01-31")


def test_eodhd_provider_rejects_missing_required_columns(monkeypatch):
    monkeypatch.setattr(
        "src.data.eodhd_provider.urllib_request.urlopen",
        lambda request, timeout: FakeResponse([{"date": "2024-01-02", "open": 10.0}]),
    )
    with pytest.raises(ProviderError, match="missing required columns"):
        EodhdProvider(api_key="test-key").get_daily_bars("AAPL.US", "2024-01-01", "2024-01-31")


def test_eodhd_provider_rejects_a_share_symbols():
    with pytest.raises(ProviderError, match="Use --provider akshare"):
        EodhdProvider(api_key="test-key").get_daily_bars("002475.SZ", "2024-01-01", "2024-01-31")
    with pytest.raises(ProviderError, match="Use --provider akshare"):
        EodhdProvider(api_key="test-key").get_daily_bars("002475", "2024-01-01", "2024-01-31")


def test_build_provider_accepts_eodhd():
    assert isinstance(build_provider("eodhd"), EodhdProvider)
