""" """
import click
from kytrade.portfolio import Portfolio
import kytrade.strategy.buy_and_hold as bah


@click.group()
def backtest():
    """Backtest strategies"""


@click.option("--start-date", "-d", required=True, help="Format: YYYY-DD-MM")
@click.option("--end-date", "-e", required=False, default=None, help="Format: YYYY-DD-MM")
@click.argument("qty")
@click.argument("ticker")
@click.command()
def buy_and_hold(ticker, qty, start_date, end_date):
    """Buy and hold a given stock"""
    click.echo(f"Backtesting buying and holding {qty} {ticker}")
    if end_date:
        click.echo(f"Holding until {end_date}")
    else:
        click.echo("Holding until most recent data")
    portfolio = Portfolio(date=start_date, balance=0)
    position = portfolio.position(ticker)
    position.buy_at_moment(qty, "open")


backtest.add_command(buy_and_hold)
