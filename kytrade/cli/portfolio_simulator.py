""" portfoliocommands """
import click

import kytrade.portfolio_simulator as ps


@click.group(name="ps")
def portfolio_simulator():
    """Portfolio Simulator"""


@click.option("--date", "-d", required=True, help="Start date  YYYY-MM-DD")
@click.argument("name")
@click.command()
def create(name, date):
    """Create a simulated portfolio instance"""
    ps.create_portfiolio_sim(name, date)
    click.echo("Done")


@click.command(name="list")
def _list():
    """list instances"""
    click.echo(ps.list_portfiolio_sims())


@click.command()
def details():
    """Print a detailed overview of a portfolio instance"""
    click.echo("TODO")


@click.argument("id")
@click.command()
def delete(id):
    """Print a detailed overview of a portfolio instance"""
    ps.delete_portfolio_sim(id)
    click.echo(f"Done")


portfolio_simulator.add_command(create)
portfolio_simulator.add_command(_list)
portfolio_simulator.add_command(details)
portfolio_simulator.add_command(delete)
