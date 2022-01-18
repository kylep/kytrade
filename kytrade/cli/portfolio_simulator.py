""" portfoliocommands """
import click

import kytrade.portfolio_simulator as ps
from kytrade.cli.common import get_table


@click.group(name="ps")
def portfolio_simulator():
    """Portfolio Simulator"""


@click.option("--date", "-d", required=True, help="Start date  YYYY-MM-DD")
@click.argument("name")
@click.command()
def create(name, date):
    """Create a simulated portfolio instance"""
    portfolio = ps.Portfolio(name, date)
    portfolio.save()
    click.echo("Done")


@click.command(name="list")
def _list():
    """list instances"""
    portfolios = ps.list_portfiolio_sims()
    table = get_table(portfolios)
    click.echo(table)


@click.command()
def details():
    """Print a detailed overview of a portfolio instance"""
    click.echo("TODO")


@click.argument("id")
@click.command()
def delete(id):
    """Print a detailed overview of a portfolio instance"""
    ps.Portfolio(id).delete()
    click.echo(f"Done")


@click.option("--usd", default=0.00, help="Dollars USD to add")
@click.argument("id")
@click.command()
def add_funds(id, usd):
    portfolio = ps.Portfolio.load(id)
    portfolio.balance += usd
    portfolio.save()


portfolio_simulator.add_command(create)
portfolio_simulator.add_command(_list)
portfolio_simulator.add_command(details)
portfolio_simulator.add_command(delete)
portfolio_simulator.add_command(add_funds)
