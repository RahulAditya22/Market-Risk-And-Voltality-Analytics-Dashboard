from __future__ import annotations

import pandas as pd
import pytest

from market_risk.validation import DataValidationError, validate_price_data


def frame(values=(100.0, 101.0, 102.0)):
    return pd.DataFrame({"Close": values}, index=pd.date_range("2026-01-01", periods=len(values)))


def test_valid_data_is_accepted():
    result = validate_price_data(frame())
    assert result.equals(frame())


@pytest.mark.parametrize(
    "bad_frame, message",
    [
        (pd.DataFrame({"Open": [1, 2]}, index=pd.date_range("2026-01-01", periods=2)), "required"),
        (pd.DataFrame({"Close": [100, 101]}), "DatetimeIndex"),
        (pd.DataFrame({"Close": [100, 101]}, index=pd.to_datetime(["2026-01-02", "2026-01-01"])), "sorted"),
        (pd.DataFrame({"Close": [100, 101]}, index=pd.to_datetime(["2026-01-01", "2026-01-01"])), "duplicate"),
        (pd.DataFrame({"Close": [100, None]}), "missing"),
        (pd.DataFrame({"Close": [100, -1]}), "positive"),
        (pd.DataFrame({"Close": [100, "bad"]}), "numeric"),
    ],
)
def test_validation_rejects_corrupt_data(bad_frame, message):
    with pytest.raises(DataValidationError, match=message):
        validate_price_data(bad_frame)


def test_validation_rejects_insufficient_data():
    with pytest.raises(DataValidationError, match="At least 2"):
        validate_price_data(frame((100.0,)), min_observations=2)
