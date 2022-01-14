""" Test the simple moving average logic"""
from pandas.core.frame import DataFrame
import kytrade.data.sma as sma


def test_calc():
    """test that sma calculates correctly"""
    data = [
        {"date": "2020-01-01", "ticker": "XYZ", "high": 10, "low": 1, "open": 9, "close": 5},
        {"date": "2020-01-02", "ticker": "XYZ", "high": 20, "low": 2, "open": 6, "close": 20},
        {"date": "2020-01-03", "ticker": "XYZ", "high": 30, "low": 3, "open": 6, "close": 101},
    ]
    df = DataFrame(data=data)
    assert sma.calc(df, "high") == 20
    assert sma.calc(df, "low") == 2
    assert sma.calc(df, "open") == 7
    assert sma.calc(df, "close") == 42
