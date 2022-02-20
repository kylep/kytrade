"""Strategy conditions

condition structure
"<name>": {
    "type": "<condition funciton name>",
    "args": {
        "<arg name>": <arg value>,
    }
}
"""
from kytrade.data.db import get_document, set_document

DOCUMENT = "conditions"


def set_condition(name: str, condition_type: str, args: dict = {}):
    """Create an condition record in the database"""
    db_conditions = get_document(DOCUMENT)
    condition = {"type": condition_type, "args": args}
    db_conditions[name] = condition
    set_document(DOCUMENT, db_conditions)


def get_conditions() -> dict:
    """Get all the saved conditions"""
    return get_document(DOCUMENT)

def delete_condition(name) -> None:
    """Remove a condition from the db"""
    db_conditions = get_document(DOCUMENT)
    if name in db_conditions:
        del db_conditions[name]
    set_document(DOCUMENT, db_conditions)


def start_of_month():
    """Start of Month condition"""
    return False
