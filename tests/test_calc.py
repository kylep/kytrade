"""Test calculations"""
import datetime
import pytest
from collections import namedtuple

from kytrade import calc


Day = namedtuple("Day", "ticker, date close")  # ...quack


@pytest.fixture
def sample_stocks():
    """Return a list of sample stocks"""
    Stock = namedtuple('Stock', 'ticker close')
    return [Stock("FOO", 10), Stock("FOO", 20), Stock("FOO", 30)]


def test_compound_anual_growth_rate():
    """test the cagr logic"""
    start_date = datetime.date.fromisoformat("2000-01-01")
    years = 3
    days = 365.25 * years
    end_date = start_date + datetime.timedelta(days=days)
    days = [
        Day("Foo", end_date, 8000),
        Day("FOO", start_date, 1000)
    ]
    assert calc.compound_anual_growth_rate(days, "close") == 100


def test_average(sample_stocks):
    """Test the 'average' logic"""
    avg = calc.average([stock.close for stock in sample_stocks])
    assert avg == 20


def test_variance(sample_stocks):
    """test variance"""
    variance = calc.variance([stock.close for stock in sample_stocks])
    assert variance == 100


def test_standard_dev(sample_stocks):
    """test standard deviation"""
    standard_deviation = calc.standard_deviation([stock.close for stock in sample_stocks])
    assert standard_deviation == 10


def test_calc_min_max_index():
    """test indexed min max"""
    data = [10,11,12,13,4,5,6,7,7,8,9]
    test_min, min_index = calc.indexed_min(data)
    assert test_min == min(data)
    assert min_index == 4


def test_max_drawdown():
    """test the max drawdown"""
    Day = namedtuple("Day", "date close")  # ...quack
    vals = [
        Day( datetime.date.fromisoformat("2000-01-10"), 110),
        Day( datetime.date.fromisoformat("2000-01-09"), 200),
        Day( datetime.date.fromisoformat("2000-01-08"), 110),
        Day( datetime.date.fromisoformat("2000-01-07"), 55),
        Day( datetime.date.fromisoformat("2000-01-06"), 50),
        Day( datetime.date.fromisoformat("2000-01-05"), 95),
        Day( datetime.date.fromisoformat("2000-01-04"), 90),
        Day( datetime.date.fromisoformat("2000-01-03"), 100),
        Day( datetime.date.fromisoformat("2000-01-02"), 10),
        Day( datetime.date.fromisoformat("2000-01-01"), 1),
    ]
    mdd = calc.max_drawdown(vals, "close")
    # raise Exception(mdd)
    assert mdd["ratio"] == -.5
