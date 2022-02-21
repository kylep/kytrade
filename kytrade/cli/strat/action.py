"""Strategy action"""
import click
from beautifultable import BeautifulTable, ALIGN_LEFT

from kytrade.strategy.action import set_action, get_actions, delete_action


@click.group()
def action():
    """Strategy Actions"""


@click.command(name="list")
def _list():
    """List the created strategy actions"""
    actions = get_actions()
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = ["Name", "Type", "Args"]
    for action_name in actions:
        table.rows.append([action_name, actions[action_name]["type"], actions[action_name]["args"]])
    click.echo(table)


@click.argument("name")
@click.command()
def delete(name):
    """Delete an action by name"""
    delete_action(name)


@click.group()
def create():
    """Create a strategy action"""


@click.option("--cash", "-c", help="Numeric percentage to rebalance into cash (USD)")
@click.option("--stock", "-s", "stocks", multiple=True, help="'<symbol>=<%>' (Multiple)")
@click.argument("name")
@click.command()
def rebalance(name, stocks, cash):
    """Create a rebalance action"""
    stocks_dict = {}
    for stock in stocks:
        split = stock.split("=")
        symbol = split[0]
        allocation = split[1]
        stocks_dict[symbol] = allocation
    args = {"stocks": stocks_dict, "cash": cash}
    set_action(name=name, action_type="rebalance", args=args)


create.add_command(rebalance)
action.add_command(_list)
action.add_command(create)
action.add_command(delete)
