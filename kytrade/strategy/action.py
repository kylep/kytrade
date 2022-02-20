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
from kytrade.data.db import get_document, set_document


DOCUMENT = "actions"


def set_action(name: str, action_type: str, args: dict = {}):
    """Create an action record in the database"""
    db_actions = get_document(DOCUMENT)
    action = {"type": action_type, "args": args}
    db_actions[name] = action
    set_document(DOCUMENT, db_actions)


def get_actions() -> dict:
    """Get all the saved actions"""
    return get_document(DOCUMENT)

def delete_action(name) -> None:
    """Remove an action from the db"""
    db_actions = get_document(DOCUMENT)
    if name in db_actions:
        del db_actions[name]
    set_document(DOCUMENT, db_actions)



def rebalance(portfolio, cash: float = 0, stocks: dict = {}):
	"""Rebalance at best effort to given percentage allocations"""
