""" Download commands """
import click
from kytrade.data.daily_stock_price import download_daily_stock_prices


@click.group()
def download():
    """Download data from upstream APIs"""


@click.argument("ticker")
@click.command()
def daily_stock_prices(ticker):
    """Save <=20 yrs of TICKER daily data to db"""
    click.echo(f"Downloading: {ticker}")
    download_daily_stock_prices(ticker)


download.add_command(daily_stock_prices)
