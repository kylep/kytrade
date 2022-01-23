"""Stock Market Simulator"""
import datetime
from collections import namedtuple

from sqlalchemy import select, desc

from kytrade import alphavantage
from kytrade.data.db import get_session
from kytrade.data.models import DailyStockPrice


class StockDataNotFound(Exception):
    """Failed to find expected share data"""


SpotPrice = namedtuple("SpotPrice", "open close")


class StockMarket:
    """Simulates the stock market
    Pre-loads stock data and stores it in memory, speeding up portfolio simulations considerably
    """
    # Class-level variables allow StockMarket to act as a singleton using borg design pattern
    # https://code.activestate.com/recipes/66531/
    daily_price_history = {}
    session = get_session()

    def __init__(self, session=None):
        """Construct a StockMarket """
        self.session = session if session else self.session

    def download_daily_price_history(self, ticker):
        """ Save the ticker data from upstream APIs to the local database"""
        daily_stock_prices = alphavantage.get_daily_stock_prices(ticker, compact=False)
        self.session.bulk_save_objects(daily_stock_prices, update_changed_only=True)
        self.session.commit()

    def select_daily_price(self, ticker=None, from_date=None, limit=0) -> list:
        """fetch saved daily price data from the daily_stock_price table"""
        query = select([DailyStockPrice]).order_by(desc(DailyStockPrice.date))
        if ticker:
            query = query.where(DailyStockPrice.ticker == ticker)
        if from_date:
            dt = datetime.date.fromisoformat(str(from_date))
            query = query.where(DailyStockPrice.date <= dt)
        if limit > 0:
            query = query.limit(limit)
        price_data = [elem[0] for elem in self.session.execute(query).all()]
        if not price_data:
            msg = f"Failed to fetch stock prices for {ticker} at {from_date} from the database"
            raise StockDataNotFound(msg)
        return price_data

    def get_spot(self, ticker: str, date: str) -> float:
        """Return the closing price for the given stock at the given day"""
        SpotPrice = namedtuple("SpotPrice", "open close")
        daily_price = self.select_daily_price(ticker=ticker, from_date=date)[0].close
        return SpotPrice(daily_price.open, daily_price.close)
