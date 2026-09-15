from __future__ import annotations

import pandas as pd


def maximum_drawdown(prices: pd.Series) -> float:
    clean = prices.dropna()
    if clean.empty:
        raise ValueError("At least one price is required for maximum drawdown.")
    running_peak = clean.cummax()
    drawdown = clean / running_peak - 1.0
    return float(drawdown.min())


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    _validate_confidence(confidence)
    clean = returns.dropna()
    if clean.empty:
        raise ValueError("At least one return is required for historical VaR.")
    threshold = float(clean.quantile(1.0 - confidence))
    return max(0.0, -threshold)


def expected_shortfall(returns: pd.Series, confidence: float = 0.95) -> float:
    _validate_confidence(confidence)
    clean = returns.dropna()
    if clean.empty:
        raise ValueError("At least one return is required for Expected Shortfall.")
    threshold = float(clean.quantile(1.0 - confidence))
    tail = clean[clean <= threshold]
    if tail.empty:
        return 0.0
    return max(0.0, -float(tail.mean()))


def _validate_confidence(confidence: float) -> None:
    if not 0.5 < confidence < 1.0:
        raise ValueError("Confidence must be greater than 0.5 and less than 1.0.")
