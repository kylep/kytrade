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
        table.rows.append(
            [condition_name, conditions[condition_name]["type"], conditions[condition_name]["args"]]
        )
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
def start_of_day(name):
    """Create a start-of-day condition"""
    set_condition(name=name, condition_type="start_of_day", args={})


@click.argument("name")
@click.command()
def start_of_month(name):
    """Create a start-of-month condition"""
    set_condition(name=name, condition_type="start_of_month", args={})


@click.argument("name")
@click.command()
def start_of_quarter(name):
    """Create a start-of-quarter condition"""
    set_condition(name=name, condition_type="start_of_quarter", args={})


@click.argument("name")
@click.command()
def start_of_year(name):
    """Create a start-of-year condition"""
    set_condition(name=name, condition_type="start_of_year", args={})


create.add_command(start_of_day)
create.add_command(start_of_month)
create.add_command(start_of_quarter)
create.add_command(start_of_year)
condition.add_command(_list)
condition.add_command(create)
condition.add_command(delete)
