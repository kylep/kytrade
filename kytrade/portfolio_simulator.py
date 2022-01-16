"""Portfolio - handles positions, balance, and time"""
import datetime
import pandas as pd
from pandas.core.frame import DataFrame
from sqlalchemy import select, delete, desc

from kytrade.data import db
from kytrade.data import models


class InsufficientFundsError(Exception):
    """Balance is too low to buy"""


class Portfolio:
    """ Portfolio Simulator """
    def __init__(self, ps_id):
        """ Instantiate a Portfolio Simulator instance from ID """
        self.session = db.session()
        self.id = ps_id
        self.models = {
            "PortfolioSimulator": self._fetch_model_portfolio_simulator()
        }
        self.name = self.models["PortfolioSimulator"].name
        self.date = self.models["PortfolioSimulator"].date
        self.usd = self.models["PortfolioSimulator"].usd

    def _fetch_model_portfolio_simulator(self):
        """Query this portfolio simulator from the database"""
        query = select(models.PortfolioSimulator).where(models.PortfolioSimulator.id == self.id)
        result = self.session.execute(query)
        row = result.one()
        return row[0]

    def advance_one_day(self, save=True):
        """Advance one day"""
        self.date += datetime.timedelta(days=1)
        print(f"{self.name} advanced to {self.date}")

    def advance_to_date(self, date: str = None):
        """Advance the date one day, or to the given date YYYY-MM-DD"""
        dt_date = datetime.date.fromisoformat(date)
        while p.date < dt_date:
            self.advance_one_day(save=False)



    @staticmethod
    def new(name: str, date: str):
        """Create a new Portfolio in the db and return its simulator object - date: YYYY-MM-DD"""
        ps_id = create_portfiolio_sim(name, date)
        return Portfolio(ps_id)


def create_portfiolio_sim(name: str, date: str) -> int:
    """Create a portfolio simulator in the database and return its index"""
    ps = models.PortfolioSimulator()
    ps.name = name
    ps.date = date
    ps.usd = 0
    session = db.session()
    session.add(ps)
    session.commit()
    session.refresh(ps)
    return ps.id


def list_portfiolio_sims() -> DataFrame:
    """List all portfolio_sims decending by date"""
    query = select(models.PortfolioSimulator).order_by(desc(models.PortfolioSimulator.date))
    return pd.read_sql(query, db.engine)




def delete_portfolio_sim(ps_id: int) -> None:
    """Delete a portfolio simulator instance"""
    session = db.session()
    statement = delete(PortfolioSimulator.PortfolioSimulator).where(models.PortfolioSimulator.id== ps_id)
    session.execute(statement)
    session.commit()
