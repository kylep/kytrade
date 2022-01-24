"""simple moving average

    ticker varchar(8), date DATE, style VARCHAR(16), days INT, value
"""
import datetime

import sqlalchemy as sqla
import pandas as pd
from pandas.core.frame import DataFrame

from kytrade.stock_market import StockMarket
from kytrade.data import db
from kytrade.data.models import DailySMA


def calc(df: DataFrame, style: str):
    """Return the SMA of a given style from the given DataFrame

    Raises TooFewEntriesError if there isn't enough data.

    supported styles:
        close
        open
        high
        low
    """
    sum_price = 0
    for row in df.itertuples():
        # ex: if style="close", add the closing price to sum_price
        sum_price += getattr(row, style)
    avg = sum_price / len(df)
    return avg


def save(ticker: str, from_date: str, days: int, style: str) -> DataFrame:
    """Save return the SMA to the database for the given date"""
    market = StockMarket()
    prices_df = market.get_daily_price(ticker=ticker, from_date=from_date, limit=days)
    if len(prices_df) != days:
        return None  # edge cases, happens on oldest data points from 1999
    value = calc(prices_df, style)
    sma_df = to_df(ticker=ticker, from_date=from_date, days=days, value=value, style=style)
    db.save_dataframe(DailySMA, sma_df)
    return sma_df


def get(ticker: str, from_date: str, days: int, style: str) -> DataFrame:
    """get the saved sma else calculate it, save it, then get it"""
    dt = datetime.date.fromisoformat(from_date)
    query = (
        sqla.select([DailySMA])
        .where(DailySMA.columns.date == dt)
        .where(DailySMA.columns.ticker == ticker)
        .where(DailySMA.columns.days == days)
        .where(DailySMA.columns.style == style)
    )
    df = pd.read_sql(query, db.engine)
    if not df.empty():
        return df
    return calc(df, style)
