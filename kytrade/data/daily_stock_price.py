""" daily price data """
import datetime

import pandas as pd
import sqlalchemy as sqla
from sqlalchemy import select, desc
from pandas.core.frame import DataFrame

from kytrade.data import db
from kytrade.data.models import DailyStockPrice
from kytrade import alphavantage


def download_daily_stock_prices(ticker) -> None:
    """Save <=20 yrs of TICKER daily data to db"""
    df = alphavantage.get_daily_stock_prices(ticker, compact=False)[0]
    df["ticker"] = ticker
    df["date"] = df.index
    db.save_dataframe(DailyStockPrice, df)


def fetch(ticker=None, from_date=None, limit=0) -> DataFrame:
    """fetch saved daily price data from the daily_stock_price table as a pandas DataFrame"""
    query = select([DailyStockPrice]).order_by(desc(DailyStockPrice.date))
    if ticker:
        query = query.where(DailyStockPrice.ticker == ticker)
    if from_date:
        dt = datetime.date.fromisoformat(from_date)
        query = query.where(DailyStockPrice.date <= dt)
    if limit > 0:
        query = query.limit(limit)
    return pd.read_sql(query, db.engine)
