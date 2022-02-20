"""Portfolio Simulator

Portfolio db structure:

metad:
"<name>": {
    "date_opened": "YYYY-MM-DD",
    "cash": <# usd (float)>,
    "stock_positions": {
        "<symbol>": <#>,
    },
    "stock_transactions": [
        {
            "date": "<YYYY-MM-DD>",
            "symbol": "<symbol>",
            "qty": <#>,
            "unit_price": <#>,
            "action": "<'BUY'/'SELL'>"
        },
    ],
    "cash_operations": [
        {
            "date": "<YYYY-MM-DD>",
            "action": "<'DEPOSIT'/'WITHDRAW'>",
            "usd": <#>
        },
    ],
    "value_history": {
        "<YYYY-MM-DD">: {
            "total_usd": <#>,
            "profit_usd": <#>
        },
    },
    "strategies": [
        "<name>"
    ],
}

"""
import datetime
from sqlalchemy import select, delete, desc, or_
from sqlalchemy.orm.attributes import flag_modified

from kytrade.data import db
from kytrade.data import models
from kytrade import exceptions as exc
from kytrade.ps import metadata
from kytrade.ps.enums import TransactionAction, CashOperationAction


def create_portfolio(
    name: str,
    date: str,
    cash: float = 0,
    stock_positions: dict = {},
    stock_transactions: list = [],
    cash_operations: list = [],
    value_history: dict = {},
    strategies: list = [],
) -> None:
    """Write portfolio state to DB"""
    dt_date = datetime.date.fromisoformat(str(date))
    data = {
        "date_opened": date,
        "cash": cash,
        "stock_positions": stock_positions,
        "stock_transactions": stock_transactions,
        "cash_operations": cash_operations,
        "value_history": value_history,
        "strategies": strategies,
    }
    portfolio = models.Portfolio(name=name, data=data, date=dt_date)
    session = db.get_session()
    session.add(portfolio)
    session.commit()


def get_portfolio(name: str) -> dict:
    """Get a specific portfolio"""
    query = select(models.Portfolio).where(models.Portfolio.name == name)
    session = db.get_session()
    session.expire_on_commit = False
    result = session.execute(query).one()
    return result[0]


def update_portfolio(portfolio: models.Portfolio):
    """Save a portfolio"""
    # SQLAlchemy doesn't notice that JSON fields change unless you flag_modified
    flag_modified(portfolio, "data")
    db.commit(portfolio)


def list_portfolios():
    """Return a list of all portfolios"""
    query = select(models.Portfolio)
    session = db.get_session()
    result = session.execute(query).all()
    return [res[0] for res in result]


def delete_portfolio(name: str):
    """Delete a portfolio"""
    portfolio = get_portfolio(name)
    db.delete(portfolio)


def log_stock_transaction(
    portfolio: models.Portfolio, symbol: str, qty: int, unit_price: float, action: TransactionAction
) -> None:
    """Log a stock transaction in given portfolio"""
    transaction = {
        "date": str(portfolio.date),
        "symbol": symbol,
        "qty": qty,
        "unit_price": unit_price,
        "action": action.value,
    }
    portfolio.data["stock_transactions"].append(transaction)


def log_cash_operation(
    portfolio: models.Portfolio, action: CashOperationAction, usd: float
) -> None:
    """Log a cash operation in given portfolio"""
    cash_operation = {"date": str(portfolio.date), "action": action.value, "usd": usd}
    portfolio.data["cash_operations"].append(cash_operation)


def log_value_history(portfolio: models.Portfolio) -> None:
    """Log the value history in given portfolio"""
    portfolio.data["value_history"][str(portfolio.date)] = {
        "total_usd": metadata.total_value(portfolio),
        "profit_usd": metadata.profit(portfolio),
    }


def add_strategy(portfolio: models.Portfolio, strategy_name: str) -> None:
    """Add a strategy to a portfolio"""
    if strategy_name not in portfolio.data["strategies"]:
        portfolio.data["strategies"].append(strategy_name)


def remove_strategy(portfolio: models.Portfolio, strategy_name: str) -> None:
    """Remove a strategy from a portfolio"""
    if strategy_name in portfolio.data["strategies"]:
        portfolio.data["strategies"].remove(strategy_name)
