from __future__ import annotations

import pandas as pd
import pytest

from market_risk.correlation import correlation_matrix, pearson_correlation, rolling_correlation


def test_correlation_aligns_timestamps():
    first = pd.Series([1.0, 2.0, 3.0], index=pd.date_range("2026-01-01", periods=3))
    second = pd.Series([10.0, 20.0, 30.0], index=pd.date_range("2026-01-02", periods=3))
    assert pearson_correlation(first, second) == pytest.approx(1.0)


def test_correlation_rejects_constant_series():
    series = pd.Series([1.0, 1.0, 1.0])
    with pytest.raises(ValueError, match="constant"):
        pearson_correlation(series, series)


def test_correlation_matrix_uses_returns():
    data = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})
    result = correlation_matrix(data)
    assert result.loc["a", "b"] == pytest.approx(-1.0)


def test_rolling_correlation():
    index = pd.date_range("2026-01-01", periods=4)
    first = pd.Series([1, 2, 3, 4], index=index)
    second = pd.Series([2, 4, 6, 8], index=index)
    result = rolling_correlation(first, second, window=2)
    assert result.iloc[-1] == pytest.approx(1.0)
