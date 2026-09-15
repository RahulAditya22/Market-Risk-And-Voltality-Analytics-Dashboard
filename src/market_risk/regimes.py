from __future__ import annotations

import pandas as pd

LOW = "LOW VOLATILITY"
MEDIUM = "MEDIUM VOLATILITY"
HIGH = "HIGH VOLATILITY"


def classify_volatility_regime(rolling_vol: pd.Series) -> pd.Series:
    clean = rolling_vol.dropna()
    if clean.empty:
        return pd.Series(index=rolling_vol.index, dtype="object")
    low_threshold = float(clean.quantile(1 / 3))
    high_threshold = float(clean.quantile(2 / 3))

    def classify(value: float) -> str:
        if pd.isna(value):
            return "UNAVAILABLE"
        if value <= low_threshold:
            return LOW
        if value <= high_threshold:
            return MEDIUM
        return HIGH

    return rolling_vol.map(classify)
