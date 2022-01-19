""" daily price data """
import datetime

from sqlalchemy import select, desc

from kytrade import alphavantage
from kytrade.data.db import get_session
from kytrade.data.models import DailyStockPrice


class StockDataNotFound(Exception):
    """Failed to find expected share data"""

def download_daily_stock_prices(ticker) -> None:
    """Save <=20 yrs of TICKER daily data to db"""
    session = get_session()
    daily_stock_prices = alphavantage.get_daily_stock_prices(ticker, compact=False)
    #for daily_stock_price in daily_stock_prices:
    #    session.add(daily_stock_price)
    session.bulk_save_objects(daily_stock_prices, update_changed_only=True)
    session.commit()


def fetch(ticker=None, from_date=None, limit=0) -> list:
    """fetch saved daily price data from the daily_stock_price table as a pandas DataFrame"""
    query = select([DailyStockPrice]).order_by(desc(DailyStockPrice.date))
    if ticker:
        query = query.where(DailyStockPrice.ticker == ticker)
    if from_date:
        dt = datetime.date.fromisoformat(str(from_date))
        query = query.where(DailyStockPrice.date <= dt)
    if limit > 0:
        query = query.limit(limit)
    price_data = [elem[0] for elem in get_session().execute(query).all()]
    if not price_data:
        msg = f"Failed to fetch stock prices for {ticker} at {from_date} from the database"
        raise StockDataNotFound(msg)
    return price_data

def spot_close_price(ticker: str, date: str) -> float:
    """Return the closing price for the given stock at the given day"""
    return fetch(ticker=ticker, from_date=date)[0].close
