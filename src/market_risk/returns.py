from __future__ import annotations

import pandas as pd

from market_risk.validation import validate_price_data


def calculate_returns(prices: pd.Series) -> pd.Series:
    if not isinstance(prices, pd.Series):
        raise TypeError("Prices must be a pandas Series.")
    frame = prices.to_frame("Close")
    validate_price_data(frame, min_observations=1)
    return prices.pct_change(fill_method=None).dropna()
