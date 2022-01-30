"""Stock Market Simulator"""
import datetime
from collections import namedtuple

from sqlalchemy import select, asc, desc, func

from kytrade import alphavantage, calc
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

    def get_metadata(self, ticker: str) -> dict:
        """Query, calculate, and return a dict of metadata about the stocks"""
        days = self.get_daily_price(ticker)  # they're in chrono order desc, [0] is newest
        close = [day.close for day in days]
        years_open = (days[0].date - days[-1].date).days / 365.25
        cagr = calc.compound_anual_growth_rate(close[-1], close[0], years_open)
        return {

            "count": len(days),
            "start": str(days[-1].date),
            "end": str(days[0].date),
            "compound_anual_growth_rate": cagr,
            "last_value": close[0],
            "high": max([day.high for day in days]),
            "low": min([day.low for day in days]),
            "20_day_average": calc.average(close[:20]),
            "200_day_average": calc.average(close[:200]),
            "all_time_average": calc.average(close),
            "20_day_variance": calc.variance(close[:20]),
            "200_day_variance": calc.variance(close[:200]),
            "all_time_variance": calc.variance(close),
            "20_day_standard_deviation": calc.standard_deviation(close[:20]),
            "200_day_standard_deviation": calc.standard_deviation(close[:200]),
            "all_time_standard_deviation": calc.standard_deviation(close),
            "20d_bollinger_band": calc.bollinger_bands(close[:20]),
            "max_drawdown": calc.max_drawdown(close)
        }


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

    def download_daily_price_history(self, ticker) -> None:
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
        else:
            # same as above, but only return up to the index indicated by the limit
            return self.daily_price_history[ticker][index : index + limit]

    def get_spot(self, ticker: str, date: str) -> float:
        """Return the closing price for the given stock at the given day"""
        daily_price = self.get_daily_price(ticker=ticker, from_date=date, limit=1)[0]
        return SpotPrice(daily_price.open, daily_price.close)
