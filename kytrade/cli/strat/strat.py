"""Strategy module"""
import click
from pprint import pprint
from beautifultable import BeautifulTable, ALIGN_LEFT

from kytrade.strategy import strategy
from kytrade.cli.strat.condition import condition
from kytrade.cli.strat.action import action


@click.group()
def strat():
    """Portfolio Strategies"""


@click.command(name="list")
def _list():
    """List portfolio strategies"""
    strategies = strategy.get_strategies()
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = ["Name", "Description", "Conditions"]
    for name in strategies:
        table.rows.append([name, strategies[name]["description"], strategies[name]["conditions"]])
    click.echo(table)


@click.argument("name")
@click.command()
def delete(name):
    """Delete a strategy"""
    strategy.delete_strategy(name)


@click.option("--description", "-d", default="", help="Description of this strategy")
@click.argument("name")
@click.command()
def create(name, description):
    """Create a strategy"""
    if name in strategy.get_strategies():
        click.echo(f"{name} already exists")
        return
    strategy.set_strategy(name, description=description)


@click.option("--action", "-a", multiple=True, required=True, help="Name of action (Multi)")
@click.option("--condition", "-c", required=True, help="Name of condition")
@click.argument("name")
@click.command()
def add_conditional_action(name, condition, action):
    """Link a condition-action pair to action to this strategy"""
    strategies = strategy.get_strategies()
    db_strategy = strategies[name] if name in strategies else None
    if not db_strategy:
        click.echo(f"Error: Strategy {name} does not exist")
        return
    actions = list(action)
    condition_mapping = strategy.condition_mapping(condition, actions)
    db_strategy["conditions"].append(condition_mapping)
    strategy.set_strategy(
        name,
        condition_mappings=db_strategy["conditions"],
        description=db_strategy["description"]
    )



strat.add_command(_list)
strat.add_command(create)
strat.add_command(condition)
strat.add_command(action)
strat.add_command(add_conditional_action)
strat.add_command(delete)
