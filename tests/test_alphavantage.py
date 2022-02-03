"""Test alphavantage.py"""
import kytrade.api.alphavantage as av


def do_thing():
    return 5


def test_get_daily_stock_prices(mock_time_series):
    orm_instances = av.get_daily_stock_prices("FOO")
    assert len(orm_instances) == 1
