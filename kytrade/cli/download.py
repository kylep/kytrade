""" Download commands """
import click
from kytrade.stock_market import StockMarket


@click.group()
def download():
    """Download data from upstream APIs"""


@click.argument("ticker")
@click.command()
def daily_stock_prices(ticker):
    """Save <=20 yrs of TICKER daily data to db"""
    click.echo(f"Downloading: {ticker}")
    StockMarket().download_daily_price_history(ticker)


download.add_command(daily_stock_prices)
