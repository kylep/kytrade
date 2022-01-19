""" portfoliocommands """
import click
from beautifultable import BeautifulTable

import kytrade.portfolio_simulator as ps


def _get_ps_table(portfolios: list):
    """Print a list of portfolios"""
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    headers = ["id", "name", "opened", "date", "balance", "num_tx", "tx_profit", "positions"]
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
            f"{portfolio.tx_profit:.2f}",
            positions,
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
    """Print a detailed overview of a portfolio instance"""
    ps.Portfolio.load(id).delete()
    click.echo(f"Done")


@click.option("--usd", default=0.00, help="Dollars USD to add")
@click.argument("id")
@click.command()
def add_funds(id, usd):
    """Add $USD to the portfolio"""
    portfolio = ps.Portfolio.load(id)
    portfolio.balance += usd
    portfolio.save()
    table = _get_ps_table([portfolio])
    click.echo(table)

@click.option("--comp/--no-comp", default=False, help="--comp for free shares")
@click.option("--close/--open", default=False, help="buy at open or close - default: open")
@click.option("--qty", "-n", required=True, help="Qty to buy")
@click.option("--ticker", "-t", required=True, help="Stock ticker")
@click.argument("id")
@click.command()
def buy_stock(id, ticker, qty, close, comp):
    """Buy qty shares of ticker """
    portfolio = ps.Portfolio.load(id)
    at = "close" if close else "open"
    portfolio.buy_stock(ticker=ticker.upper(), qty=int(qty), at=at, comp=comp)
    portfolio.save()
    table = _get_ps_table([portfolio])
    click.echo(table)

@click.option("--close/--open", default=False, help="buy at open or close - default: open")
@click.option("--qty", "-n", required=True, help="Qty to buy")
@click.option("--ticker", "-t", required=True, help="Stock ticker")
@click.argument("id")
@click.command()
def sell_stock(id, ticker, qty, close):
    """Sell qty shares of ticker """
    portfolio = ps.Portfolio.load(id)
    at = "close" if close else "open"
    portfolio.sell_stock(ticker=ticker.upper(), qty=int(qty), at=at)
    portfolio.save()
    table = _get_ps_table([portfolio])
    click.echo(table)


portfolio_simulator.add_command(create)
portfolio_simulator.add_command(_list)
portfolio_simulator.add_command(details)
portfolio_simulator.add_command(delete)
portfolio_simulator.add_command(add_funds)
portfolio_simulator.add_command(buy_stock)
portfolio_simulator.add_command(sell_stock)
