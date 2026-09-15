from __future__ import annotations

import pandas as pd

from market_risk.plotting import (
    correlation_heatmap,
    drawdown_chart,
    price_chart,
    return_distribution_chart,
    rolling_correlation_chart,
    rolling_volatility_chart,
)


def test_plotting_functions_return_figures():
    index = pd.date_range("2026-01-01", periods=4)
    prices = pd.Series([100.0, 102.0, 101.0, 105.0], index=index)
    returns = prices.pct_change().dropna()
    matrix = pd.DataFrame({"A": [1.0, 0.5], "B": [0.5, 1.0]}, index=["A", "B"])

    assert price_chart(prices, "Price").data
    assert rolling_volatility_chart(returns.rolling(2).std(), "Volatility").data
    assert return_distribution_chart(returns, 0.02).data
    assert drawdown_chart(prices).data
    assert correlation_heatmap(matrix).data
    assert rolling_correlation_chart(pd.Series([0.1, 0.2], index=index[:2])).data
