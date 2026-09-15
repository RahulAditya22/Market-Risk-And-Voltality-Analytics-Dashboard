from __future__ import annotations

import pandas as pd

from market_risk.regimes import HIGH, LOW, MEDIUM, classify_volatility_regime


def test_regime_classification_is_explainable():
    values = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05, 0.06], index=pd.RangeIndex(6))
    result = classify_volatility_regime(values)
    assert result.iloc[0] == LOW
    assert result.iloc[-1] == HIGH
    assert MEDIUM in set(result)


def test_empty_regime_series_is_unavailable():
    result = classify_volatility_regime(pd.Series(dtype=float))
    assert result.empty
