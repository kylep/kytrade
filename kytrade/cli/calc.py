""" kytrade CLI entrypoint """
import click
import kytrade.data.sma as sma


@click.group()
def calc():
    """Calculations"""


@click.option("--all/--no-all", "-a" "all_dates", default=False, help="Calulate for all dates")
@click.option(
    "--style",
    "-s",
    required=False,
    default="close",
    help="[close, open, high, low], default: close",
)
@click.option("--days", "-d", required=True, help="# of days back to calc SMA")
@click.option("--from-date", "f", required=True, help="start date YYYY-MM-DD ex: '2020-01-01'")
@click.argument("ticker")
@click.command()
def sma(ticker, from_datedays, style, all_dates):
    """simple moving avage"""
    pass
    # sma_df = sma.get(ticker, fro


calc.add_command(sma)
