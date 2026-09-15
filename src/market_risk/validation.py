from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ("Close",)


class DataValidationError(ValueError):
    """Raised when historical market data violates the internal contract."""


def validate_price_data(data: pd.DataFrame, min_observations: int = 2) -> pd.DataFrame:
    if not isinstance(data, pd.DataFrame):
        raise DataValidationError("Market data must be a pandas DataFrame.")
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise DataValidationError(f"Missing required columns: {', '.join(missing)}")
    if not isinstance(data.index, pd.DatetimeIndex):
        raise DataValidationError("Market data must use a DatetimeIndex.")
    if data.index.has_duplicates:
        raise DataValidationError("Market data contains duplicate timestamps.")
    if not data.index.is_monotonic_increasing:
        raise DataValidationError("Market data timestamps must be sorted ascending.")
    prices = data["Close"]
    if not pd.api.types.is_numeric_dtype(prices):
        raise DataValidationError("Close prices must be numeric.")
    if prices.isna().any():
        raise DataValidationError("Close prices contain missing values.")
    if (prices <= 0).any():
        raise DataValidationError("Close prices must be positive.")
    if len(data) < min_observations:
        raise DataValidationError(
            f"At least {min_observations} observations are required; received {len(data)}."
        )
    return data.copy()
