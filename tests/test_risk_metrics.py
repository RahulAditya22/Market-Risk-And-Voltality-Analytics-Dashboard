from __future__ import annotations

import pandas as pd
import pytest

from market_risk.risk_metrics import expected_shortfall, historical_var, maximum_drawdown


def test_maximum_drawdown():
    prices = pd.Series([100.0, 120.0, 90.0, 110.0, 80.0])
    assert maximum_drawdown(prices) == pytest.approx(-1 / 3)


def test_var_is_positive_loss_magnitude():
    returns = pd.Series([-0.10, -0.05, 0.01, 0.02])
    assert historical_var(returns, 0.75) == pytest.approx(0.0625)


def test_expected_shortfall_averages_tail_losses():
    returns = pd.Series([-0.10, -0.05, 0.01, 0.02])
    assert expected_shortfall(returns, 0.75) == pytest.approx(0.10)


@pytest.mark.parametrize("confidence", [0.5, 1.0, 0.1])
def test_invalid_confidence_rejected(confidence):
    with pytest.raises(ValueError, match="Confidence"):
        historical_var(pd.Series([-.1, .1]), confidence)


def test_all_positive_tail_has_zero_loss_magnitude():
    returns = pd.Series([0.01, 0.02, 0.03, 0.04])
    assert historical_var(returns, 0.95) == 0.0
    assert expected_shortfall(returns, 0.95) == 0.0
