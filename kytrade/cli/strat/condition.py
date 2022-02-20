"""Strategy conditions"""
import click
from beautifultable import BeautifulTable, ALIGN_LEFT

from kytrade.strategy.condition import set_condition, get_conditions, delete_condition


@click.group()
def condition():
    """Strategy Conditions"""


@click.command(name="list")
def _list():
    """List strategy conditions"""
    conditions = get_conditions()
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = ["Name", "Type", "Args"]
    for condition_name in conditions:
        table.rows.append([condition_name, conditions[condition_name]["type"], conditions[condition_name]["args"]])
    click.echo(table)


@click.argument("name")
@click.command()
def delete(name):
    """Delete a condition"""
    delete_condition(name)


@click.group()
def create():
    """Create a strategy"""


@click.argument("name")
@click.command()
def start_of_month(name):
    """Create a start-of-month condition
    This type of condition has no arguments, start of month is start of month
    """
    set_condition(name=name, condition_type="start_of_month", args={})


create.add_command(start_of_month)
condition.add_command(_list)
condition.add_command(create)
condition.add_command(delete)
