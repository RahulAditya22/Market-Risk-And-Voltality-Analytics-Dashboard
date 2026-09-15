from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def price_fixture() -> pd.Series:
    index = pd.date_range("2026-01-01", periods=6, freq="D")
    return pd.Series([100.0, 102.0, 101.0, 105.0, 103.0, 106.0], index=index, name="Close")
