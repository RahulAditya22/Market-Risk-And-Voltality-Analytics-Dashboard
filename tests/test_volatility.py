from __future__ import annotations

import math

import pandas as pd
import pytest

from market_risk.volatility import annualized_volatility, downside_volatility, rolling_volatility


def test_rolling_volatility_uses_sample_std():
    returns = pd.Series([0.01, 0.02, 0.03, 0.04])
    result = rolling_volatility(returns, window=2)
    assert result.iloc[1] == pytest.approx(pd.Series([0.01, 0.02]).std())
    assert result.iloc[0] != result.iloc[0]


def test_annualized_volatility():
    returns = pd.Series([0.01, 0.02, 0.03])
    expected = returns.std(ddof=1) * math.sqrt(252)
    assert annualized_volatility(returns) == pytest.approx(expected)


def test_zero_volatility_for_constant_returns():
    assert annualized_volatility(pd.Series([0.01, 0.01])) == pytest.approx(0.0)


def test_downside_volatility_only_uses_negative_returns():
    returns = pd.Series([-0.02, 0.01, -0.04, 0.03])
    assert downside_volatility(returns) == pytest.approx(pd.Series([-0.02, -0.04]).std(ddof=1))


def test_invalid_window_rejected():
    with pytest.raises(ValueError, match="at least 2"):
        rolling_volatility(pd.Series([0.1, 0.2]), window=1)
