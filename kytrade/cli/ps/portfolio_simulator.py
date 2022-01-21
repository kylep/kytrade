""" portfoliocommands """
import click
from beautifultable import BeautifulTable

import kytrade.portfolio_simulator as ps
from kytrade.cli.ps.tx import tx


def _get_ps_table(portfolios: list):
    """Print a list of portfolios"""
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    headers = ["id", "name", "opened", "date", "cash", "num_tx", "total", "positions", "profit"]
    for portfolio in portfolios:
        positions = ", ".join([f"{pos.ticker}({pos.qty})" for pos in portfolio.stock_positions])
        num_transactions = len(portfolio.stock_transactions)
        row = [
            portfolio.id,
            portfolio.name,
            str(portfolio.orm_ps.opened),
            str(portfolio.date),
            f"{portfolio.balance:.2f}",
            num_transactions,
            f"{portfolio.value_at_close:.2f}",
            positions,
            f"{portfolio.profit:.2f}"
        ]
        table.rows.append(row)
    table.columns.header = headers
    return table


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
    table = _get_ps_table([portfolio])
    click.echo(table)


@click.command(name="list")
def _list():
    """list instances"""
    portfolios = ps.list_portfolios()
    table = _get_ps_table(portfolios)
    click.echo(table)


@click.command()
def details():
    """Print a detailed overview of a portfolio instance"""
    click.echo("TODO")


@click.argument("id")
@click.command()
def delete(id):
    """Delete a portfolio"""
    ps.Portfolio.load(id).delete()
    click.echo(f"Done")


@click.option("--to-date", "-d", required=False, default=None, help="Advance to date YYYY-MM-DD")
@click.argument("id")
@click.command()
def advance(id, to_date):
    """Advance the ps 1 day or to --to-date"""
    portfolio = ps.Portfolio.load(id)
    if to_date:
        portfolio.advance_to_date(to_date)
    else:
        portfolio.advance_one_day()
    portfolio.save()


portfolio_simulator.add_command(create)
portfolio_simulator.add_command(_list)
portfolio_simulator.add_command(details)
portfolio_simulator.add_command(delete)
portfolio_simulator.add_command(advance)
portfolio_simulator.add_command(tx)
