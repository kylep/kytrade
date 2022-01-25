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
        """Construct a StockMarket"""
        self.session = session if session else self.session

    def download_daily_price_history(self, ticker):
        """Save the ticker data from upstream APIs to the local database"""
        daily_stock_prices = alphavantage.get_daily_stock_prices(ticker, compact=False)
        self.session.bulk_save_objects(daily_stock_prices, update_changed_only=True)
        self.session.commit()

    def select_daily_price(self, ticker=None, from_date=None, limit=0, lazy_load=True) -> list:
        """query saved daily price data from the daily_stock_price table"""
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
            if lazy_load and ticker:
                self.download_daily_price_history(ticker)
                price_data = [elem[0] for elem in self.session.execute(query).all()]
            else:
                msg = f"Failed to fetch stock prices for {ticker} at {from_date} from the database"
                raise StockDataNotFound(msg)
        return price_data

    def get_daily_price(self, ticker, from_date=None, limit=0) -> list:
        """Return lazy-loaded price data"""
        # Lazy-load the price data
        # self.select_daily_price[ticker][0] is the newest, [-1] is the oldest
        if ticker not in self.daily_price_history:
            self.daily_price_history[ticker] = self.select_daily_price(ticker=ticker)
        if from_date:
            # Find the first price entry going forward from from_date
            dated_entry = next(
                (
                    entry
                    for entry in self.daily_price_history[ticker]
                    if entry.date <= datetime.date.fromisoformat(str(from_date))
                )
            )
        else:
            dated_entry = self.daily_price_history[ticker][0]  # already sorted by date, descending
        index = self.daily_price_history[ticker].index(dated_entry)
        if limit == 0:
            # return all data starting from the index of the given date
            return self.daily_price_history[ticker][index:]
        else:
            # same as above, but only return up to the index indicated by the limit
            return self.daily_price_history[ticker][index:index+limit]

    def get_spot(self, ticker: str, date: str) -> float:
        """Return the closing price for the given stock at the given day"""
        daily_price = self.get_daily_price(ticker=ticker, from_date=date, limit=1)[0]
        return SpotPrice(daily_price.open, daily_price.close)
