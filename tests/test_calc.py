"""Test calculations"""
from collections import namedtuple
import pytest
from kytrade import calc


@pytest.fixture
def sample_stocks():
    """Return a list of sample stocks"""
    Stock = namedtuple('Stock', 'ticker close')
    return [Stock("FOO", 10), Stock("FOO", 20), Stock("FOO", 30)]

def test_compound_anual_growth_rate():
    """test the cagr logic"""
    # Assumption, 12 years at 6% doubles a value
    # verifying...
    years = 3
    start = 1000
    end = 8000
    verify_cagr = 100
    test_cagr = (verify_cagr/100+1) ** years * start  # double start 3 times, 2, 4, 8...
    assert test_cagr == end
    assert calc.compound_anual_growth_rate(start, end, years) == verify_cagr


def test_stock_close_average(sample_stocks):
    """Test the stock_close_average logic"""
    avg = calc.stock_close_average(sample_stocks)
    assert avg == 20


def test_stock_close_variance(sample_stocks):
    """test stock_close_variance"""
    variance = calc.stock_close_variance(sample_stocks)
    two_thirds_percent = 2/3*100
    # Really gotta sort out Pythons weird floating point problem
    assert variance == 66.66666666666667


def test_stocks_close_standard_dev(sample_stocks):
    """test stocks_close_standard_dev"""
    standard_deviation = calc.stocks_close_standard_dev(sample_stocks)
    # TODO: Get someone to check if this is actually right...
    assert standard_deviation == 8.16496580927726
