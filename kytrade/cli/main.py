""" kytrade CLI entrypoint """
import sys
import click
from kytrade.const import VERSION
from kytrade.cli.stockmarket import sm
from kytrade.cli.init import init
from kytrade.cli.strat.strat import strat
from kytrade.cli.ps.portfolio_simulator import portfolio_simulator as ps


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
shell.add_command(sm)
shell.add_command(init)
shell.add_command(ps)
shell.add_command(strat)
