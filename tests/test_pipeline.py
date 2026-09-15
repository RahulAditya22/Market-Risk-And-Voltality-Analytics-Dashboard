from __future__ import annotations

import pandas as pd

from market_risk.correlation import pearson_correlation
from market_risk.returns import calculate_returns
from market_risk.risk_metrics import expected_shortfall, historical_var, maximum_drawdown
from market_risk.validation import validate_price_data
from market_risk.volatility import annualized_volatility, rolling_volatility


def test_deterministic_analytics_pipeline():
    index = pd.date_range("2026-01-01", periods=8)
    prices = pd.DataFrame(
        {"Close": [100.0, 102.0, 101.0, 105.0, 103.0, 106.0, 104.0, 108.0]},
        index=index,
    )

    validated = validate_price_data(prices)
    returns = calculate_returns(validated["Close"])
    rolling = rolling_volatility(returns, window=3)

    assert len(returns) == 7
    assert rolling.notna().sum() == 5
    assert annualized_volatility(returns) > 0
    assert maximum_drawdown(validated["Close"]) < 0
    assert historical_var(returns, 0.95) >= 0
    assert expected_shortfall(returns, 0.95) >= 0

    comparison = pd.Series(
        [0.01, 0.02, -0.01, 0.03, -0.02, 0.01, -0.01], index=returns.index
    )
    assert -1 <= pearson_correlation(returns, comparison) <= 1
