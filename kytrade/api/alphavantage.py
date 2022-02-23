""" alphavantage stock api

    api docs:   https://www.alphavantage.co/documentation/
    py lib:     https://github.com/RomelTorres/alpha_vantage
"""
from alpha_vantage.timeseries import TimeSeries

from kytrade.data import models
from kytrade.const import ALPHAVANTAGE_API_KEY


def get_daily_stock_prices(ticker: str, compact=False) -> list:
    """Return a list of models.DailyStockPrice objects"""
    outputsize = "compact" if compact else "full"
    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY)
    daily_vals = ts.get_daily(ticker, outputsize=outputsize)
    orm_instances = []
    for date, values in daily_vals[0].items():
        orm_instance = models.DailyStockPrice()
        orm_instance.ticker = ticker
        orm_instance.date = date
        orm_instance.open = values["1. open"]
        orm_instance.high = values["2. high"]
        orm_instance.low = values["3. low"]
        orm_instance.close = values["4. close"]
        orm_instance.volume = values["5. volume"]
        orm_instances.append(orm_instance)
    return orm_instances
