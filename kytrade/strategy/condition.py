"""Strategy conditions

condition structure
"<name>": {
    "type": "<condition funciton name>",
    "args": {
        "<arg name>": <arg value>,
    }
}
"""
from kytrade.data import models
from kytrade.data.db import get_document, set_document
from kytrade.exceptions import InvalidStrategyConditionName

DOCUMENT = "conditions"
CACHE = {}



def set_condition(name: str, condition_type: str, args: dict = {}):
    """Create an condition record in the database"""
    db_conditions = get_document(DOCUMENT)
    condition = {"type": condition_type, "args": args}
    db_conditions[name] = condition
    set_document(DOCUMENT, db_conditions)


def get_conditions() -> dict:
    """Get all the saved conditions"""
    return get_document(DOCUMENT)


def get_condition(name: str) -> dict:
    """Return one condition by name"""
    return get_conditions()[name]


def delete_condition(name) -> None:
    """Remove a condition from the db"""
    db_conditions = get_document(DOCUMENT)
    if name in db_conditions:
        del db_conditions[name]
    set_document(DOCUMENT, db_conditions)


def start_of_day(portfolio):
    """Start of day condition"""
    return True  # We only work with daily conditions rn


def start_of_month(portfolio):
    """Start of Month condition"""
    return portfolio.date.day == 1


def start_of_quarter(portfolio):
    """Start of quarter condition"""
    return (portfolio.date.month % 3 == 0 and portfolio.date.day == 1)


def start_of_year(portfolio):
    """Start of year condition"""
    return (portfolio.date.month == 1 and portfolio.date.day == 1)


def check_condition(portfolio: models.Portfolio, condition_name: str, args: dict = {}) -> bool:
    """Execute a condition function and return if it passes"""
    # maybe use a dict or enum with values as the functions for this kinda like a switch?
    if condition_name == "start_of_day":
        return start_of_day(portfolio)
    elif condition_name == "start_of_month":
        return start_of_month(portfolio)
    elif condition_name == "start_of_quarter":
        return start_of_quarter(portfolio)
    elif condition_name == "start_of_year":
        return start_of_year(portfolio)
    else:
        raise InvalidStrategyConditionName(condition_name)
