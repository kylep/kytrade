"""Transactions"""
import click
from beautifultable import BeautifulTable
from pprint import pprint

import kytrade.ps.portfolio as ps
import kytrade.ps.tx as ptx
from kytrade.data import models
from kytrade.data import db


@click.group()
def tx():
    """Transactions"""


@click.argument("name")
@click.command(name="list")
def _list(name):
    """List the transactions"""
    portfolio = ps.get_portfolio(name)
    pprint(portfolio.data["stock_transactions"])
    for tx in portfolio.data["stock_transactions"]:
        buy = f"{tx['date']} - {tx['action']} {tx['qty']} {tx['symbol']}"
        total = float(tx["unit_price"]) * float(tx["qty"])
        deets = f"@ ${tx['unit_price']:,.2f} for ${total:,.2f}"
        click.echo(f"{buy} {deets}")


@click.option("--comp/--no-comp", default=False, help="--comp for free shares")
@click.option("--qty", "-n", required=True, help="Qty to buy")
@click.option("--symbol", "-s", required=True, help="Stock ticker")
@click.argument("name")
@click.command()
def buy_stock(name, symbol, qty, comp):
    """Buy qty shares of ticker"""
    portfolio = ps.get_portfolio(name)
    ptx.buy_stock(portfolio, symbol, int(qty), comp)
    ps.update_portfolio(portfolio)


@click.option("--cost", "-c", required=True, help="Max cost of shares")
@click.option("--symbol", "-s", required=True, help="Stock symbol")
@click.argument("name")
@click.command()
def buy_stock_by_price(name, symbol, cost):
    """Buy as many shares as can be afforded by price at cost"""
    portfolio = ps.get_portfolio(name)
    ptx.buy_stock_by_cost(portfolio, symbol, float(cost))
    ps.update_portfolio(portfolio)


@click.option("--qty", "-n", required=True, help="Qty to buy")
@click.option("--symbol", "-s", required=True, help="Stock ticker")
@click.argument("name")
@click.command()
def sell_stock(name, symbol, qty):
    """Sell qty shares of ticker"""
    portfolio = ps.get_portfolio(name)
    ptx.sell_stock(portfolio, symbol, int(qty))
    ps.update_portfolio(portfolio)


@click.option("--usd", default=0.00, help="Dollars USD to add")
@click.argument("name")
@click.command()
def deposit(name, usd):
    """Deposit $USD into the portfolio"""
    portfolio = ps.get_portfolio(name)
    ptx.deposit(portfolio, float(usd))
    ps.update_portfolio(portfolio)


@click.option("--usd", default=0.00, help="Dollars USD to add")
@click.argument("name")
@click.command()
def withdraw(name, usd):
    """Withdraw $USD from the portfolio"""
    portfolio = ps.get_portfolio(name)
    ptx.withdraw(portfolio, usd)
    ps.update_portfolio(portfolio)


tx.add_command(_list)
tx.add_command(buy_stock)
tx.add_command(buy_stock_by_price)
tx.add_command(sell_stock)
tx.add_command(deposit)
tx.add_command(withdraw)
