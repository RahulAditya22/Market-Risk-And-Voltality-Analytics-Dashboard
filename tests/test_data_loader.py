from __future__ import annotations

import pandas as pd
import pytest

import market_risk.data_loader as loader
from market_risk.data_loader import MarketDataError, asset_ticker, fetch_price_data


def valid_download():
    return pd.DataFrame(
        {"Close": [100.0, 101.0, 102.0]}, index=pd.date_range("2026-01-01", periods=3)
    )


def test_data_loader_normalizes_valid_provider_data(monkeypatch):
    monkeypatch.setattr(loader.yf, "download", lambda *args, **kwargs: valid_download())
    result = fetch_price_data("TEST", "2026-01-01", "2026-01-05")
    assert list(result.columns) == ["Close"]
    assert len(result) == 3


def test_data_loader_handles_empty_response(monkeypatch):
    monkeypatch.setattr(loader.yf, "download", lambda *args, **kwargs: pd.DataFrame())
    with pytest.raises(MarketDataError, match="No market data"):
        fetch_price_data("TEST", "2026-01-01", "2026-01-05")


def test_data_loader_handles_provider_exception(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("rate limited")

    monkeypatch.setattr(loader.yf, "download", fail)
    with pytest.raises(MarketDataError, match="could not be retrieved"):
        fetch_price_data("TEST", "2026-01-01", "2026-01-05")


def test_data_loader_handles_malformed_response(monkeypatch):
    bad = pd.DataFrame({"Open": [1, 2]}, index=pd.date_range("2026-01-01", periods=2))
    monkeypatch.setattr(loader.yf, "download", lambda *args, **kwargs: bad)
    with pytest.raises(MarketDataError, match="Close"):
        fetch_price_data("TEST", "2026-01-01", "2026-01-05")


def test_asset_ticker_mapping():
    assert asset_ticker("Gold") == "GC=F"
    assert asset_ticker("USD/INR") == "USDINR=X"
    with pytest.raises(ValueError, match="Unknown asset"):
        asset_ticker("Unknown")
