
import datetime
from sqlalchemy import select, delete, desc

from kytrade.data.db import get_session
from kytrade.data import models
from kytrade.data import daily_stock_price


class InsufficientFundsError(Exception):
    """Balance is too low to buy"""

class InsufficientSharesError(Exception):
    """Can't remove shares you don't have"""

class Portfolio:
    """ Portfolio Simulator """
    def __init__(self, name: str, date: str):
        """ Instantiate a new Portfolio Simulator instance """
        ps = models.PortfolioSimulator()
        ps.name = name
        ps.date = datetime.date.fromisoformat(str(date))
        ps.usd = 0
        ps.opened = ps.date
        self.session = get_session()
        self.orm_ps = ps  # The DB portfolio_simulators row in ObjectRelationalModel format
        self.orm_stock_positions = []
        self.orm_stock_transactions = []
        self.id = None  # Until saved
        self.on_open = []   # list of Strategy's to execute on market open
        self.on_close = []  # ...to execute on market close
        self.positions = []  # list of open SharePosition instances

    @staticmethod
    def load(ps_id):
        """Create a new Portfolio in the db and return its simulator object - date: YYYY-MM-DD"""
        query = select(models.PortfolioSimulator).where(models.PortfolioSimulator.id == ps_id)
        session = get_session()
        orm_ps = session.execute(query).one()[0]
        instance = Portfolio(orm_ps.name, orm_ps.date)
        instance.session = session
        instance.orm_ps = orm_ps
        return instance

    @property
    def balance(self):
        """how much money's left?"""
        return self.orm_ps.usd

    @balance.setter
    def balance(self, value):
        """Set the portfolio balance - raise InsufficientFundsError if negative"""
        # Reminder: When implementing logging, log changes to balance
        self.orm_ps.usd = value
        if value < 0:
            raise InsufficientFundsError(f"Portfolio balance {value} is negative")

    @property
    def date(self):
        """Get the Portfolio date from the orm"""
        return self.orm_ps.date

    @property
    def name(self):
        """Get the Portfolio from the orm"""
        return self.orm_ps.name

    @property
    def stock_positions(self):
        """Get the stock positions - read from DB on first query"""
        if not self.orm_stock_positions:
            query = (
                select(models.PortSimStockPosition)
                .where(models.PortSimStockPosition.portfolio_id == self.orm_ps.id)
            )
            positions = self.session.execute(query).all()
            self.orm_stock_positions = positions
        return self.orm_stock_positions

    @property
    def stock_transactions(self):
        """List of PortSimStockTransaction orm objects"""
        if not self.orm_stock_transactions:
            pass


    def delete(self):
        """Delete this portfolio simulator instance"""
        self.session.delete(self.orm["PortfolioSimulator"])
        self.session.commit()

    def advance_one_day(self):
        """Advance one day"""
        self.orm_ps.date += datetime.timedelta(days=1)
        print(f"{self.orm_ps.name} advanced to {self.orm_ps.date}")

    def advance_to_date(self, date: str = None):
        """Advance the date one day, or to the given date YYYY-MM-DD"""
        dt_date = datetime.date.fromisoformat(date)
        while self.orm_ps.date < dt_date:
            self.advance_one_day()

    def add_stock(self, ticker, qty):
        """Add shares, creating a new position if needed"""
        position = next((pos for pos in self.stock_positions if pos.ticker == ticker), None)
        if not position:
            position = models.PortSimStockPosition(ticker=ticker, qty=0)
            self.orm_stock_positions.append(position)
        position.qty += qty


    def remove_stock(self, ticker, qty):
        """Remove shares, but keep the position option with 0 qty

           Raise InsufficientSharesError if not enough shares exist
        """
        position = next((pos for pos in self.stock_positions if pos.ticker == ticker), None)
        current_qty = position.qty if position else 0
        new_qty = current_qty - qty
        if not position or new_qty < 0:
            raise InsufficientSharesError(f"Can't remove {qty} x {ticker}: have {current_qty}")
        position.qty = new_qty

    def buy_stock(self, ticker:str, qty: int, at: str, price=None):
        """Add shares and subtract the cost from the balance - exception if overdrawn
           at: open, close, price
        """
        dsp = daily_stock_price.fetch(ticker, from_date=self.date, limit=1)[0]
        price = price if price else getattr(dsp, at)
        self.balance -= (price * qty)
        self.add_stock(ticker, qty)

    def sell_stock(self, ticker: str, qty: int, at: str, price):
        """Sell shares and add the total to the balance - exception if shares are not owned
           at: open, close, price
        """
        dsp = daily_stock_price.fetch(ticker, from_date=self.date, limit=1)[0]
        price = price if price else getattr(dsp, at)
        self.remove_stock(ticker, qty)
        self.balance += (price * qty)

    def save(self):
        """Save this portfolio instance to the database"""
        self.session.add(self.orm_ps)
        for orm_position in self.orm_stock_positions:
            self.session.add(orm_position)
        self.session.commit()
        self.session.refresh(self.orm_ps)  # refresh adds the .id property




def list_portfiolio_sims() -> list:
    """List all portfolio_sims decending by date"""
    query = select(models.PortfolioSimulator).order_by(desc(models.PortfolioSimulator.date))
    # fix the return data - the returned list is of 1-element tupples initially
    return [elem[0] for elem in get_session().execute(query).all()]
