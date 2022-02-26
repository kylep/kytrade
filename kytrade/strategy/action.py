"""Strategy actions

action structure:

"<name>": {
  "type": "<action function name>",
  "args": {
    "<arg name>": <arg value>,
  }
}

note to self: I don't like this method of making things pluggable. The possibility for argument
missmatches seems like a pain in the ass. Maybe refactor but not sure what into.
"""
from kytrade.data import models
from kytrade.data.db import get_document, set_document
from kytrade.exceptions import InvalidStrategyActionName, InvalidTotalPortfolioAllocationPercentage
from kytrade.ps import tx
from kytrade.ps import metadata


DOCUMENT = "actions"
CACHE = {}


def set_action(name: str, action_type: str, args: dict = {}):
    """Create an action record in the database"""
    db_actions = get_document(DOCUMENT)
    action = {"type": action_type, "args": args}
    db_actions[name] = action
    set_document(DOCUMENT, db_actions)


def get_actions() -> dict:
    """Get all the saved actions"""
    return get_document(DOCUMENT)


def get_action(name: str) -> dict:
    """Get one aciton by name"""
    return get_actions()[name]


def delete_action(name) -> None:
    """Remove an action from the db"""
    db_actions = get_document(DOCUMENT)
    if name in db_actions:
        del db_actions[name]
    set_document(DOCUMENT, db_actions)


def _assert_total_alloc_percent(percents: list, target: int) -> None:
    """Assert the allocation percentage (sum of percents list) equals target else raise exc"""
    total_percents = sum(percents)
    if total_percents != target:
        err = f"{total_percents} != {target}"
        raise InvalidTotalPortfolioAllocationPercentage(f"{total_percents} != {target}")


def execute_action(portfolio: models.Portfolio, action_name: str, args: dict = {}) -> None:
    """Execute the named action with the given args in the given portfolio"""
    # same as condition, use some better mapping eventually
    if action_name == "rebalance":
        cash = float(args["cash"]) if args["cash"] else 0
        tx.rebalance_stock_positions(portfolio, cash_pct=cash, stocks=args["stocks"])
    else:
        raise InvalidStrategyActionName(action_name)
