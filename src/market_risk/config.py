from __future__ import annotations

from dataclasses import dataclass

TRADING_DAYS_PER_YEAR = 252
DEFAULT_VOLATILITY_WINDOW = 21
DEFAULT_VAR_CONFIDENCE = 0.95
MIN_OBSERVATIONS = 2


@dataclass(frozen=True)
class Asset:
    name: str
    ticker: str
    currency: str


ASSETS = {
    "Gold": Asset("Gold", "GC=F", "USD"),
    "Crude Oil": Asset("Crude Oil", "CL=F", "USD"),
    "S&P 500": Asset("S&P 500", "^GSPC", "USD"),
    "Nasdaq": Asset("Nasdaq", "^IXIC", "USD"),
    "EUR/USD": Asset("EUR/USD", "EURUSD=X", "USD"),
    "USD/INR": Asset("USD/INR", "USDINR=X", "INR"),
}

TICKERS = {name: asset.ticker for name, asset in ASSETS.items()}
