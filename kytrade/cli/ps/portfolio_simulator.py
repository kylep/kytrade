""" portfoliocommands """
import json
import click
import datetime
from beautifultable import BeautifulTable, ALIGN_LEFT
from pprint import pprint

import kytrade.ps.portfolio as ps
import kytrade.strategy
from kytrade import calc
from kytrade.ps import metadata
from kytrade.ps import simulator
from kytrade.cli.ps.tx import tx
from kytrade.cli.ps.strat import strat


def _get_ps_table(portfolios: list):
    """Print a list of portfolios"""
    table = BeautifulTable(maxwidth=140)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    headers = ["Name", "Start", "End", "Positions", "Value", "CAGR %", "MDD %", "Sharpe"]
    table.columns.header = headers
    for portfolio in portfolios:
        print(f" CALC: {portfolio.name}                           ", end="\r")
        sp = portfolio.data["stock_positions"]
        positions = ",".join([f"{key}={sp[key]}" for key in sp.keys()])
        date = str(portfolio.date)
        row = [
            portfolio.name,
            portfolio.data["date_opened"],
            str(portfolio.date),
            positions,
            f"{portfolio.data['metadata'][date]['total_value']:,.2f}",
            f"{portfolio.data['metadata'][date]['cagr']:.2f}",
            f"{portfolio.data['metadata'][date]['max_draw_down']['percent']:.2f}",
            f"{portfolio.data['metadata'][date]['sharpe_ratio']:.2f}",
        ]
        table.rows.append(row)
    return table


@click.group(name="ps")
def portfolio_simulator():
    """Portfolio Simulator"""


@click.option("--date", "-d", required=True, help="Start date  YYYY-MM-DD")
@click.argument("name")
@click.command()
def create(name, date):
    """Create a simulated portfolio instance"""
    ps.create_portfolio(name, date)
    portfolio = ps.get_portfolio(name, detailed=True)
    table = _get_ps_table([portfolio])
    click.echo(table)


@click.option("--details/--names", default=True, help="Use --names to only print names")
@click.command(name="list")
def _list(details):
    """list instances"""
    portfolios = ps.list_portfolios(detailed=details)
    if details:
        table = _get_ps_table(portfolios)
        click.echo(table)
        return
    for portfolio in portfolios:
        click.echo(portfolio.name)


@click.argument("name")
@click.command()
def describe(name):
    """Print a detailed overview of a portfolio instance"""
    portfolio = ps.get_portfolio(name, detailed=True)
    click.echo(json.dumps(portfolio.data, indent=2, default=str))


@click.argument("name")
@click.command()
def delete(name):
    """Delete a portfolio"""
    ps.delete_portfolio(name)


@click.option("--print-status/--no-print-status", default=True, help="Print sim status")
@click.option("--to-date", "-d", required=False, default=None, help="Advance to date YYYY-MM-DD")
@click.argument("name")
@click.command()
def advance(name, to_date, print_status):
    """Advance the ps 1 day or to --to-date"""
    portfolio = ps.get_portfolio(name)
    if to_date:
        simulator.advance_to_date(portfolio, to_date)
    else:
        simulator.advance_one_day(portfolio)
    ps.update_portfolio(portfolio)


@click.argument("name")
@click.command()
def value_history(name):
    """Print the balance history"""
    portfolio = ps.get_portfolio(name)
    pprint(portfolio.data["value_history"])


portfolio_simulator.add_command(create)
portfolio_simulator.add_command(_list)
portfolio_simulator.add_command(describe)
portfolio_simulator.add_command(delete)
portfolio_simulator.add_command(advance)
portfolio_simulator.add_command(tx)
portfolio_simulator.add_command(strat)
portfolio_simulator.add_command(value_history)
