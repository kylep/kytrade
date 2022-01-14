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
    click.echo(f"Saving {ticker} to DB")
    download_daily_stock_prices(ticker)
    click.echo(f"Saved daily history for {ticker}")


download.add_command(daily_stock_prices)
