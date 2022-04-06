""" Stock Market (sm) commands """
import click
import json
from pprint import pprint
from beautifultable import BeautifulTable, ALIGN_LEFT

from kytrade.stockmarket import StockMarket, INDEXES
from kytrade.data.models import Stock


@click.group()
def sm():
    """Stock Market"""


@click.command()
def screener():
    """List the daily stocks in DB"""
    sm = StockMarket()
    table = BeautifulTable(maxwidth=150, default_alignment=ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = [
        "Ticker",
        "Start",
        "End",
        "CAGR",
        "MDD",
        "ATH",
        "Close",
        "sma.20",
        "sma.200",
        "σ².20",
        "σ².200",
        "bbands",
    ]
    for ticker, meta in sm.metadata.items():
        row = [
            ticker,
            meta["start"],
            meta["end"],
            f"{meta['compound_anual_growth_rate']:.2f}%",
            f"{meta['max_drawdown']['percent']:,.2f}%",
            f"${meta['high']:,.2f}",
            f"${meta['last_value']:,.2f}",
            f"${meta['20_day_average']:,.2f}",
            f"${meta['200_day_average']:,.2f}",
            f"{meta['20_day_variance']:.2f}%",
            f"{meta['200_day_variance']:.2f}%",
            f"{meta['20d_bollinger_band']['status']}",
        ]
        table.rows.append(row)
    click.echo(table)


@click.argument("ticker")
@click.command()
def describe(ticker):
    sm = StockMarket()
    meta = sm.get_metadata(ticker)
    click.echo(json.dumps(meta, indent=2, default=str))


@click.argument("ticker")
@click.command()
def download_daily_stock_prices(ticker):
    """Save <=20 yrs of TICKER daily data to db"""
    click.echo(f"Downloading: {ticker}")
    StockMarket().download_daily_price_history(ticker)


@click.option("--ticker", required=False, default=None, help="Ticker to filter to")
@click.option(
    "--from-date", "-d", required=False, default=None, help="Year to search from, YYYY-MM-DD"
)
@click.option("--limit", required=False, default=0, help="Number of values to return")
@click.command()
def print_daily_prices(ticker, from_date, limit):
    """Print daily stock prices from DB"""
    daily_stock_prices = StockMarket().get_daily_price(
        ticker=ticker, from_date=from_date, limit=limit
    )
    table = BeautifulTable(maxwidth=120, default_alignment=ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = ["ticker", "date", "low", "high", "open", "close"]
    for dsp in daily_stock_prices:
        table.rows.append([dsp.ticker, str(dsp.date), dsp.low, dsp.high, dsp.open, dsp.close])
    click.echo(table)


@click.argument("path")
@click.command()
def load_datahub_stocks(path):
    """Populate the Stocks table with entries from datahub.io JSON outputs"""
    index = next((match for match in INDEXES if match in path), None)
    if not index:
        click.echo(f"ERROR: filename must contain one of {supported_filenames}")
        return
    click.echo(f"Importing {index} stocks from {path} - please wait...")
    StockMarket().load_stocks_from_datahub_file(path)


@click.option("--symbols/--full", default=False, help="Use --symbol to only print symbols")
@click.command()
def list_stocks(symbols):
    """Print the stocks saved to the DB"""
    stocks = StockMarket().stocks
    if symbols:
        for stock in stocks:
            click.echo(stock.ticker)
        return
    table = BeautifulTable(maxwidth=150, default_alignment=ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = [
        "Symbol",
        "Name",
        "Indexes",
        "Metadata",
    ]
    for stock in stocks:
        table.rows.append([stock.ticker, stock.name, stock.indexes_csv, stock.attributes_json])
    click.echo(table)


sm.add_command(download_daily_stock_prices)
sm.add_command(screener)
sm.add_command(print_daily_prices)
sm.add_command(describe)
sm.add_command(load_datahub_stocks)
sm.add_command(list_stocks)
