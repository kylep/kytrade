""" kytrade CLI entrypoint """
import sys
import click
from kytrade.const import VERSION
from kytrade.cli.calc import calc
from kytrade.cli.pprint import pprint
from kytrade.cli.download import download
from kytrade.cli.init import init
from kytrade.cli.backtest import backtest


if sys.version_info[0] < 3:
    sys.stderr.write("ERROR: Python 2 is not supported - use Python 3\n")
    sys.exit(1)


@click.group()
def shell():
    """Click entrypoint"""


@click.command()
def version():
    """Return the current version"""
    click.echo(VERSION)


shell.add_command(version)
shell.add_command(pprint)
shell.add_command(download)
shell.add_command(init)
shell.add_command(calc)
shell.add_command(backtest)
