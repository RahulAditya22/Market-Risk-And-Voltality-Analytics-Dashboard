from __future__ import annotations

import math

import pandas as pd

from market_risk.config import TRADING_DAYS_PER_YEAR


def rolling_volatility(returns: pd.Series, window: int = 21) -> pd.Series:
    if window < 2:
        raise ValueError("Volatility window must be at least 2.")
    if not isinstance(returns, pd.Series):
        raise TypeError("Returns must be a pandas Series.")
    return returns.rolling(window=window, min_periods=window).std(ddof=1)


def annualized_volatility(returns: pd.Series) -> float:
    clean = returns.dropna()
    if len(clean) < 2:
        raise ValueError("At least two returns are required for annualized volatility.")
    return float(clean.std(ddof=1) * math.sqrt(TRADING_DAYS_PER_YEAR))


def downside_volatility(returns: pd.Series) -> float:
    downside = returns.dropna()
    downside = downside[downside < 0]
    if len(downside) < 2:
        return 0.0
    return float(downside.std(ddof=1))
