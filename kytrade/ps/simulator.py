"""Simulator actions for the portfolio"""
import datetime
import kytrade.ps.portfolio as ps
from kytrade.data import models
from kytrade.ps import metadata
from kytrade.strategy import strategy


def add_strategy(portfolio: models.Portfolio, strategy_name: str) -> None:
    """Add a strategy to a portfolio"""
    if strategy_name not in portfolio.data["strategies"]:
        portfolio.data["strategies"].append(strategy_name)


def remove_strategy(portfolio: models.Portfolio, strategy_name: str) -> None:
    """Remove a strategy from a portfolio"""
    if strategy_name in portfolio.data["strategies"]:
        portfolio.data["strategies"].remove(strategy_name)


def advance_one_day(portfolio: models.Portfolio) -> None:
    """Advance the portfolio a day, executing any strategic actions"""
    ps.log_value_history(portfolio)
    portfolio.date += datetime.timedelta(days=1)
    for strategy_name in portfolio.data["strategies"]:
        strategy.execute_strategy(portfolio, strategy_name)



def advance_to_date(portfolio: models.Portfolio, date: str) -> None:
    """Advance to the given date in YYYY-MM-DD format"""
    dt_date = datetime.date.fromisoformat(date)
    last_date_str = str(portfolio.date)[:7]
    while portfolio.date < dt_date:
        advance_one_day(portfolio)
        date_str = str(portfolio.date)[:7]
        if date_str != last_date_str:
            last_date_str = date_str
            print(date_str, end='\r')
    print('')
