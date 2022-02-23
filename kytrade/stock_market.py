"""Stock Market Simulator"""
import json
import datetime
from collections import namedtuple

from sqlalchemy import select, desc, delete

from kytrade import calc

# from kytrade.api import alphavantage
from kytrade.api import yahoo
from kytrade.data.db import get_session
from kytrade.data.models import DailyStockPrice, Stock


class StockDataNotFound(Exception):
    """Failed to find expected share data"""


SpotPrice = namedtuple("SpotPrice", "open close")
INDEXES = ["nasdaq100", "sp500"]


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

    def get_metadata(self, ticker: str) -> dict:
        """Query, calculate, and return a dict of metadata about the stocks"""
        days = self.get_daily_price(ticker)  # they're in chrono order desc, [0] is newest
        value_attr = "close"
        return calc.get_metadata(days, value_attr)

    @property
    def metadata(self) -> dict:
        """Query, calculate, and return a dict of metadata about all stocks"""
        meta = {}
        for ticker in self.saved_tickers:
            meta[ticker] = self.get_metadata(ticker)
        return meta

    @property
    def saved_tickers(self) -> list:
        """Return a list of saved tickers"""
        ticker_query = select(DailyStockPrice.ticker).distinct()
        return [elem[0] for elem in self.session.execute(ticker_query).all()]

    @property
    def stocks(self) -> list:
        """Return a list of saved Stock db entries"""
        rows = self.session.execute(select(Stock))
        return [row[0] for row in rows]  # de-tupple

    def download_daily_price_history(self, ticker) -> None:
        """Save the ticker data from upstream APIs to the local database"""
        daily_stock_prices = yahoo.get_daily_stock_history(ticker)
        delete_query = delete(DailyStockPrice).where(DailyStockPrice.ticker == ticker)
        self.session.execute(delete_query)
        self.session.bulk_save_objects(daily_stock_prices, update_changed_only=False)
        self.session.commit()

    def load_stocks_from_datahub_file(self, path):
        """Load a datahub stock export into the 'stocks' table"""
        index = next((match for match in INDEXES if match in path), None)
        with open(path, "r", encoding="utf8") as fil:
            data = json.load(fil)
        for entry in data:
            symbol = entry["Symbol"]
            entry.pop("Symbol", None)
            name = "?"
            for name_attr in ["Name", "Company Name"]:
                if name_attr in entry:
                    name = entry[name_attr]
                    entry.pop(name_attr, None)  # removes it from metadata/attribute_json
                    break
            for spam_attr in ["Security Name", "Round Lot Size", "Test Issue"]:
                entry.pop(spam_attr, None)  # spam attributes add no value
            attributes_json = json.dumps(entry)
            stock = Stock(
                ticker=symbol, name=name, attributes_json=attributes_json, indexes_csv=index
            )
            query = select(Stock).where(Stock.ticker == symbol)
            row = self.session.execute(query).one_or_none()
            if row:
                # If the stock already exists in the db...
                db_stock = row[0]
                stock_indexes = db_stock.indexes_csv.split(",")
                update = False
                if index not in stock_indexes:
                    # check if this is a different index and update the index csv string
                    stock_indexes.append(index)
                    db_stock.indexes_csv = ",".join(stock_indexes)
                    update = True
                if attributes_json != db_stock.attributes_json:
                    # also check if there's another other metadata about this stock and add it
                    update = True
                    stock_attrs = json.loads(attributes_json)
                    db_stock_attrs = json.loads(db_stock.attributes_json)
                    for key in stock_attrs:
                        db_stock_attrs[key] = stock_attrs[key]
                    db_stock.attributes_json = json.dumps(db_stock_attrs)
                if update:
                    self.session.add(db_stock)
            else:
                self.session.add(stock)
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

    def get_oldest_price(self, ticker) -> datetime.date:
        """Return the oldest date of a saved stock"""
        return min([stock.date for stock in self.get_daily_price(ticker)])

    def get_daily_price(self, ticker, from_date=None, limit=0) -> list:
        """Return pre-cached price data"""
        if from_date:
            dt_date = datetime.date.fromisoformat(str(from_date))
            oldest_price = self.get_oldest_price(ticker)
            if dt_date < oldest_price:
                err = f"Data on {ticker} not available at {from_date} - earliest is {oldest_price}"
                raise StockDataNotFound(err)
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
        # same as above, but only return up to the index indicated by the limit
        return self.daily_price_history[ticker][index : index + limit]

    def get_spot(self, ticker: str, date: str) -> float:
        """Return the closing price for the given stock at the given day"""
        daily_price = self.get_daily_price(ticker=ticker, from_date=date, limit=1)[0]
        return SpotPrice(daily_price.open, daily_price.close)
