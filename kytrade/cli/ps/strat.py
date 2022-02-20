"""Portfolio Strategies"""
import click
from pprint import pprint
from beautifultable import BeautifulTable

import kytrade.ps.portfolio as ps
from kytrade.ps import simulator
from kytrade.data import models


@click.group()
def strat():
    """Portfolio Strategies"""


@click.argument("portfolio_name")
@click.command(name="list")
def _list(portfolio_name):
    """List the strategies in a portfolio"""
    portfolio = ps.get_portfolio(portfolio_name)
    pprint(portfolio.data["strategies"])


@click.argument("strat_name")
@click.argument("portfolio_name")
@click.command()
def add(portfolio_name, strat_name):
    """Associate a strategy with a portfolio"""
    portfolio = ps.get_portfolio(portfolio_name)
    simulator.add_strategy(portfolio, strat_name)
    ps.update_portfolio(portfolio)


@click.argument("strat_name")
@click.argument("portfolio_name")
@click.command()
def remove(portfolio_name, strat_name):
    """Dissacociate a strategy from a portfolio"""
    portfolio = ps.get_portfolio(portfolio_name)
    simulator.remove_strategy(portfolio, strat_name)
    ps.update_portfolio(portfolio)


strat.add_command(_list)
strat.add_command(add)
strat.add_command(remove)
