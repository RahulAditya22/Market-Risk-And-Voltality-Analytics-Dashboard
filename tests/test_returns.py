from __future__ import annotations

import pandas as pd
import pytest

from market_risk.returns import calculate_returns


def test_returns_match_hand_calculation(price_fixture):
    result = calculate_returns(price_fixture)
    expected = pd.Series(
        [0.02, -1 / 102, 4 / 101, -2 / 105, 3 / 103],
        index=price_fixture.index[1:],
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_returns_reject_non_series():
    with pytest.raises(TypeError):
        calculate_returns(pd.DataFrame({"Close": [1, 2]}))
