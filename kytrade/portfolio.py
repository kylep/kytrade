"""Portfolio - handles positions, balance, and time"""
import datetime

import kytrade.data.daily_stock_price as dsp
from kytrade.strategy.strategy import BaseDailyStrategy


class InsufficientFundsError(Exception):
    """Balance is too low to buy"""


class SharePosition:
    """Represents a portfolio share position"""
    def __init__(self, ticker: str):
        """Represents a portfolio share position"""
        self.ticker = ticker
        self.qty = 0
        self.book_cost = 0

    @property
    def cost_basis(self) -> float:
        """Total USD invested in this position"""
        return self.qty / self.book_cost

    def buy_at_moment(self, qty, date, moment):
        """Buy qty shares at open

        daily_df accepts a df row from daily_stock_price for price data
        moment is either open or close
        """
        if moment not in ["open", "close"]:
            raise NotImplementedError(f"unsupported moment {moment}")
        df = dsp.fetch(ticker=self.ticker, from_date=date, limit=1)
        share_price = getattr(df, moment)
        self.book_cost += share_price * qty
        self.qty += qty


class Portfolio:
    """Portfolio instance to handle positions, balance, and time"""
    def __init__(self, date: str, balance: float):
        """Portfolio instances handle positions, balance, and time

        date in YYYY-MM-DD
        balance is in USD
        """
        self.share_positions = {}
        self._balance = balance
        self.date = datetime.date.fromisoformat(date)
        self.daily_strategy = BaseDailyStrategy(self)  # override for different behaviour

    @property
    def balance(self):
        """USD cash balance of the portfolio"""
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        """Balances may not become negative"""
        if new_balance < 0:
            raise InsufficientFundsError(f"new balance would be {new_balance}")
        self._balance = new_balance

    def position(self, ticker):
        """Return a current SharePosition"""
        if ticker not in self.share_positions:
            self.share_positions[ticker] = SharePosition(ticker)
        return self.share_positions[ticker]

    # def forward_day(self):
    #     """Progress one day in time"""

    # def forward_to(self, date: str):
    #     """Forward to the given date YYYY-MM-DD"""
