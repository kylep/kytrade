"""Transactions"""
import click
from beautifultable import BeautifulTable

import kytrade.portfolio_simulator as ps


@click.group()
def tx():
    """Transactions"""


@click.argument("id")
@click.command(name="list")
def _list(id):
    """List the transactions"""
    portfolio = ps.Portfolio.load(id)
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    headers = ["date", "ticker", "qty", "unit_price", "action", "total"]
    running_total = 0
    for tx in portfolio.stock_transactions:
        multiplier = 1 if tx.action == "SELL" else -1
        total = multiplier * tx.qty* tx.unit_price
        running_total += total
        row = [tx.date, tx.ticker, tx.qty, tx.unit_price, tx.action, total]
        table.rows.append(row)
    table.rows.append(["-"]*5+[running_total])
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


tx.add_command(_list)
tx.add_command(buy_stock)
tx.add_command(sell_stock)
