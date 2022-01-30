""" Stock Market (sm) commands """
import click
from beautifultable import BeautifulTable, ALIGN_LEFT

from kytrade.stock_market import StockMarket


@click.group()
def sm():
    """Stock Market"""


@click.command()
def list_daily():
    """List the stocks in DB"""
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
        mdd = f"{meta['max_drawdown']['percent']:,.2f}% - from {meta['max_drawdown']['peak']} to {meta['max_drawdown']['trough']}",
        row = [
            ticker,
            meta["start"],
            meta["end"],
            f"{meta['compound_anual_growth_rate']:.2f}%",
            mdd,
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
def describe_stock(ticker):
    sm = StockMarket()
    prices = sm.get_daily_price(ticker)
    meta = prices.metadata
    click.echo(ticker)



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


sm.add_command(download_daily_stock_prices)
sm.add_command(list_daily)
sm.add_command(print_daily_prices)
sm.add_command(describe_stock)
