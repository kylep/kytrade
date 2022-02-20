"""Trading Strategy

Strategy structure:

"<name>": {
    "description": "<optional description>",
    "conditions": [
        "name": "<name>",
        "actions": [
            "<action name>",
        ],
    },
}
"""

from kytrade.data.db import get_document, set_document
from kytrade.strategy import action
from kytrade.strategy import condition


ACTIONS = {"rebalance": action.rebalance}
CONDITIONS = {"start_of_month": condition.start_of_month}
DOCUMENT = "strategies"


def condition_mapping(condition_name, actions: list) -> dict:
    """Return a dict linking a condition to some actions"""
    return {
        "name": condition_name,
        "actions": actions
    }


def set_strategy(name: str, condition_mappings: list = [], description: str = ""):
    """Create an action record in the database"""
    db_strategies = get_document(DOCUMENT)
    strategy = {"description": description, "conditions": condition_mappings}
    db_strategies[name] = strategy
    set_document(DOCUMENT, db_strategies)


def get_strategies() -> dict:
    """Get all the saved strategies"""
    return get_document(DOCUMENT)


def delete_strategy(name) -> None:
    """Remove a strategy from the db"""
    db_strategies = get_document(DOCUMENT)
    if name in db_strategies:
        del db_strategies[name]
    set_document(DOCUMENT, db_strategies)



