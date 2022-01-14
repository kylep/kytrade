""" Initialization commands """
import click
from kytrade.data.db import init_create_tables


@click.group()
def init():
    """Environment init cmds"""


@click.command()
def database_tables():
    """Create database tables"""
    init_create_tables()
    click.echo("Done creating tables")


init.add_command(database_tables)
