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

from kytrade.data import models
from kytrade.data.db import get_document, set_document
from kytrade.strategy import action
from kytrade.strategy import condition


DOCUMENT = "strategies"
CACHE = {}  # experimental approach to not running get_document over and over


def condition_mapping(condition_name, actions: list) -> dict:
    """Return a dict linking a condition to some actions"""
    return {"name": condition_name, "actions": actions}


def set_strategy(name: str, condition_mappings: list = [], description: str = ""):
    """Create an action record in the database"""
    db_strategies = get_document(DOCUMENT)
    strategy = {"description": description, "conditions": condition_mappings}
    db_strategies[name] = strategy
    set_document(DOCUMENT, db_strategies)


def get_strategies() -> dict:
    """Get all the saved strategies"""
    return get_document(DOCUMENT)


def get_strategy(name) -> dict:
    return get_strategies()[name]


def delete_strategy(name) -> None:
    """Remove a strategy from the db"""
    db_strategies = get_document(DOCUMENT)
    if name in db_strategies:
        del db_strategies[name]
    set_document(DOCUMENT, db_strategies)


def execute_strategy(portfolio: models.Portfolio, strategy_name):
    """execute the given strategy against the portfolio
    When the portfolio sim is looping through time this can be a real bottleneck since get_document
    runs over and over again. A module-level dictionary called CACHE persists the results to speed
    things up in that specific scenario.
    """
    if strategy_name not in CACHE:
        strat = get_strategy(strategy_name)
        CACHE[strategy_name] = strat
    else:
        strat = CACHE[strategy_name]
    for condition_data in strat["conditions"]:
        if condition_data["name"] not in condition.CACHE:
            cond = condition.get_condition(condition_data["name"])
            condition.CACHE[condition_data["name"]] = cond
        else:
            cond = condition.CACHE[condition_data["name"]]
        cond_result = condition.check_condition(portfolio, cond["type"], cond["args"])
        if not cond_result:
            return
        for action_name in condition_data["actions"]:
            if action_name not in action.CACHE:
                actn = action.get_action(action_name)
                action.CACHE[action_name] = actn
            else:
                actn = action.CACHE[action_name]
            print(actn)
            action.execute_action(portfolio, actn["type"], actn["args"])

