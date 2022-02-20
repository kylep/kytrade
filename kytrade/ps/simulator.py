"""Simulator actions for the portfolio"""
import datetime
from kytrade.data import models
from kytrade.ps import metadata


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
    print("DO THE THING")
    return
    ps.log_value_historu(portfolio)
    portfolio.date += datetime.timedelta(days=1)


def advance_to_date(portfolio: models.Portfolio, date: str) -> None:
    """Advance to the given date in YYYY-MM-DD format"""
    dt_date = datetime.date.fromisoformat(date)
    while portfolio.date < dt_date:
        advance_one_day(portfolio)
