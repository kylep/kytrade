
import datetime
from sqlalchemy import select, delete, desc

from kytrade.data.db import get_session
from kytrade.data import models


class InsufficientFundsError(Exception):
    """Balance is too low to buy"""


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
        # Reminder: When implementing logging, log changes to balance
        self.orm_ps.usd = value

    def save(self):
        """Save this portfolio instance to the database"""
        self.session.add(self.orm_ps)
        self.session.commit()
        self.session.refresh(self.orm_ps)  # refresh adds the .id property

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

    def add_shares(self):
        """Add shares, creating a new position if needed"""



def list_portfiolio_sims() -> list:
    """List all portfolio_sims decending by date"""
    query = select(models.PortfolioSimulator).order_by(desc(models.PortfolioSimulator.date))
    # fix the return data - the returned list is of 1-element tupples initially
    return [elem[0] for elem in get_session().execute(query).all()]
