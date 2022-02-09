"""Transactions"""
import click
from beautifultable import BeautifulTable

import kytrade.portfolio_simulator as ps
from kytrade.data import models


@click.group()
def tx():
    """Transactions"""


@click.argument("id")
@click.command(name="list")
def _list(id):
    """List the transactions"""
    portfolio = ps.Portfolio.load(id)
    all_tx = portfolio.stock_transactions + portfolio.cash_operations
    all_tx.sort(key=lambda obj: obj.date)
    for tx in all_tx:
        if isinstance(tx, models.PortSimStockTransaction):
            tx_total = tx.unit_price * tx.qty
            click.echo(
                f"{tx.date}  -  {tx.action}\t"
                f"{tx.qty} {tx.ticker} @ ${tx.unit_price:.2f} for ${tx_total:.2f}"
            )
        elif isinstance(tx, models.PortSimCashOperation):
            click.echo(f"{tx.date}  -  {tx.action}\t${tx.usd:.2f}")


@click.option("--comp/--no-comp", default=False, help="--comp for free shares")
@click.option("--close/--open", default=True, help="buy at open or close - default: close")
@click.option("--qty", "-n", required=True, help="Qty to buy")
@click.option("--ticker", "-t", required=True, help="Stock ticker")
@click.argument("id")
@click.command()
def buy_stock(id, ticker, qty, close, comp):
    """Buy qty shares of ticker"""
    portfolio = ps.Portfolio.load(id)
    at = "close" if close else "open"
    portfolio.buy_stock(ticker=ticker.upper(), qty=int(qty), at=at, comp=comp)
    portfolio.save()


@click.option("--cost", "-c",  required=True, help="Max cost of shares")
@click.option("--ticker", "-t", required=True, help="Stock symbol")
@click.argument("id")
@click.command()
def buy_stock_by_price(id, ticker, cost):
    """Buy as many shares as can be afforded by price at cost"""
    portfolio = ps.Portfolio.load(id)
    portfolio.buy_stock_by_price(ticker, cost)
    portfolio.save()


@click.option("--close/--open", default=False, help="buy at open or close - default: open")
@click.option("--qty", "-n", required=True, help="Qty to buy")
@click.option("--ticker", "-t", required=True, help="Stock ticker")
@click.argument("id")
@click.command()
def sell_stock(id, ticker, qty, close):
    """Sell qty shares of ticker"""
    portfolio = ps.Portfolio.load(id)
    at = "close" if close else "open"
    portfolio.sell_stock(ticker=ticker.upper(), qty=int(qty), at=at)
    portfolio.save()


@click.option("--usd", default=0.00, help="Dollars USD to add")
@click.argument("id")
@click.command()
def deposit(id, usd):
    """Deposit $USD into the portfolio"""
    portfolio = ps.Portfolio.load(id)
    portfolio.deposit(usd)
    portfolio.save()


@click.option("--usd", default=0.00, help="Dollars USD to add")
@click.argument("id")
@click.command()
def withdraw(id, usd):
    """Withdraw $USD from the portfolio"""
    portfolio = ps.Portfolio.load(id)
    portfolio.withdraw(usd)
    portfolio.save()


tx.add_command(_list)
tx.add_command(buy_stock)
tx.add_command(buy_stock_by_price)
tx.add_command(sell_stock)
tx.add_command(deposit)
tx.add_command(withdraw)
