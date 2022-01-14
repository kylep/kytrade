""" alphavantage stock api

    api docs:   https://www.alphavantage.co/documentation/
    py lib:     https://github.com/RomelTorres/alpha_vantage
"""
import os
import sys

from pandas.core.frame import DataFrame
from alpha_vantage.timeseries import TimeSeries

from kytrade.const import ALPHAVANTAGE_API_KEY


def get_daily_stock_prices(ticker, compact=False):
    """Return the daily history of a given ticker - compact returns the most recent 1000 points"""
    outputsize = "compact" if compact else "full"
    # pylint: disable-msg=W0632
    # W0632: ts.get_daily does not return a tuple with 3 entries when output_format == pandas
    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format="pandas")
    df, metadata = ts.get_daily(ticker, outputsize=outputsize)
    df = DataFrame(df)
    # fix the pandas columns to remove numeric prefixes: "1. open" -> "open"
    df_cols = [i.split(" ")[1] for i in df.columns]
    df.columns = df_cols
    return (df, metadata)
