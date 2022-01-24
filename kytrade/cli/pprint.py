""" Print commands """
import click
from kytrade.stock_market import StockMarket
from kytrade.cli.common import get_table


@click.group(name="print")
def pprint():
    """Print saved data"""


@click.option("--ticker", required=False, default=None, help="Ticker to filter to")
@click.option(
    "--from-date", "-d", required=False, default=None, help="Year to search from, YYYY-MM-DD"
)
@click.option("--limit", required=False, default=0, help="Number of values to return")
@click.command()
def daily_prices(ticker, from_date, limit):
    """Print the saved prices data"""
    daily_stock_prices = StockMarket().get_daily_price(
        ticker=ticker, from_date=from_date, limit=limit
    )
    table = get_table(daily_stock_prices)
    click.echo(table)


pprint.add_command(daily_prices)
