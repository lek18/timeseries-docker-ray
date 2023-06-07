import pandas as pd
import pytest
from app.ml.utils import get_future_dates


@pytest.mark.parametrize(
    "param",
    [
        (pd.Timestamp("2021-01-01"), "daily"),  # Test case 1
        (pd.Timestamp("2021-01-01"), "weekly"),  # Test case 2
        (pd.Timestamp("2021-01-01"), "monthly"),  # Test case 3
    ],
)
def test_get_future_dates(param):
    # Unpack the parameter values
    max_date, time_frame = param

    # Call your function with the parameter values
    result = get_future_dates(max_date, time_frame)

    if time_frame == "daily":
        # Check that the end dates is specific to the 6 months ahead
        assert result[0] == "2021-01-02" and result[-1] == "2021-07-02"
        assert len(result) == 182

    if time_frame == "weekly":
        # Check that the end dates is specific to the 6 months ahead
        # the first week is week 53 and 6 months ahead is 27
        # weeks starting from 1 out of 53- > 53,1,2,3..., 27
        assert result[0] == "2021_1" and result[-1] == "2021_26"
        assert len(result) == 26

    if time_frame == "monthly":
        # Check that the end dates is specific to the 6 months ahead
        # the first month will be 2 and last month will be 8
        assert result[0] == "2021_2" and result[-1] == "2021_7"
        assert len(result) == 6


def test_get_future_dates_raiseException():
    max_date, time_frame = pd.Timestamp("2021-01-01"), "fake_timeframe"
    with pytest.raises(Exception):
        get_future_dates(max_date, time_frame)
