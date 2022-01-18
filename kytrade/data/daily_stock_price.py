""" daily price data """
import datetime

from sqlalchemy import select, desc

from kytrade import alphavantage
from kytrade.data.db import get_session
from kytrade.data.models import DailyStockPrice


def download_daily_stock_prices(ticker) -> None:
    """Save <=20 yrs of TICKER daily data to db"""
    session = get_session()
    daily_stock_prices = alphavantage.get_daily_stock_prices(ticker, compact=False)
    for daily_stock_price in daily_stock_prices:
        session.add(daily_stock_price)
    session.commit()


def fetch(ticker=None, from_date=None, limit=0) -> list:
    """fetch saved daily price data from the daily_stock_price table as a pandas DataFrame"""
    query = select([DailyStockPrice]).order_by(desc(DailyStockPrice.date))
    if ticker:
        query = query.where(DailyStockPrice.ticker == ticker)
    if from_date:
        dt = datetime.date.fromisoformat(from_date)
        query = query.where(DailyStockPrice.date <= dt)
    if limit > 0:
        query = query.limit(limit)
    return [elem[0] for elem in get_session().execute(query).all()]
