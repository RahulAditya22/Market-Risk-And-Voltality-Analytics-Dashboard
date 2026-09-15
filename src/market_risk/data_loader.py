from __future__ import annotations

from datetime import date

import pandas as pd
import yfinance as yf

from market_risk.config import TICKERS
from market_risk.validation import DataValidationError, validate_price_data


class MarketDataError(RuntimeError):
    """Raised when live market data cannot be retrieved or validated."""


def fetch_price_data(
    ticker: str, start: date | str, end: date | str, min_observations: int = 2
) -> pd.DataFrame:
    try:
        data = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=False,
            progress=False,
            threads=False,
        )
    except Exception as exc:  # provider errors are intentionally normalized here
        raise MarketDataError("Live market data could not be retrieved.") from exc

    if data is None or data.empty:
        raise MarketDataError("No market data was returned for the selected period.")

    if isinstance(data.columns, pd.MultiIndex):
        close_columns = [
            column for column in data.columns if "Close" in {str(level) for level in column}
        ]
        if not close_columns:
            raise MarketDataError("The market-data response does not contain Close prices.")
        data = data.loc[:, close_columns]
        data.columns = ["Close"]
    else:
        if "Close" not in data.columns:
            raise MarketDataError("The market-data response does not contain Close prices.")
        data = data[["Close"]]

    try:
        return validate_price_data(data, min_observations=min_observations)
    except DataValidationError as exc:
        raise MarketDataError(f"Market data failed validation: {exc}") from exc


def asset_ticker(asset_name: str) -> str:
    try:
        return TICKERS[asset_name]
    except KeyError as exc:
        raise ValueError(f"Unknown asset: {asset_name}") from exc
