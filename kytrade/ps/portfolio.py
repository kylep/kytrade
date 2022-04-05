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
    "metadata": {
        "<YYYY-MM-DD>": {
            "total_value": #,
            "cagr": #,
            "max_draw_down": {
              "peak": #,
              "peak_date": "YYYY-MM-DD",
              "trough": #,
              "trough_date": "YYYY-MM-DD",
              "ratio": #,
              "percent": #,
              "absolute": #,
            },
            "sharpe_ratio": #,
        },
    },
}

"""
# TODO: remove date_opened, value_history's first entry covers it
import datetime
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from kytrade.data import db
from kytrade.data import models
from kytrade.ps import metadata
from kytrade import calc
from kytrade.ps.enums import TransactionAction, CashOperationAction


def create_portfolio(
    name: str,
    date: str,
    cash: float = 0,
    stock_positions: dict = None,
    stock_transactions: list = None,
    cash_operations: list = None,
    value_history: dict = None,
    strategies: list = None,
    metadata: dict = None,
) -> None:
    """Write portfolio state to DB"""
    # (W0511) Setting arguments as lists/dicts is dangerous - this is so tedious...
    # https://stackoverflow.com/questions/26320899/why-is-the-empty-dictionary-a-dangerous-default-value-in-python
    stock_positions = stock_positions if stock_positions else {}
    stock_transactions = stock_transactions if stock_transactions else []
    cash_operations = cash_operations if cash_operations else []
    value_history = value_history if value_history else {}
    strategies = strategies if strategies else []
    metadata = metadata if metadata else {}
    # /W0511 fixup
    dt_date = datetime.date.fromisoformat(str(date))
    data = {
        "date_opened": date,
        "cash": cash,
        "stock_positions": stock_positions,
        "stock_transactions": stock_transactions,
        "cash_operations": cash_operations,
        "value_history": value_history,
        "strategies": strategies,
        "metadata": metadata,
    }
    portfolio = models.Portfolio(name=name, data=data, date=dt_date)
    session = db.get_session()
    session.add(portfolio)
    session.commit()


def set_metadata(portfolio: models.Portfolio) -> None:
    """Calculate the metadata at the current date for given portfolio"""
    value_days = metadata.value_days_history_named_tuples(portfolio)
    cagr = calc.compound_anual_growth_rate(value_days, value_attr="total")
    mdd = calc.max_drawdown(value_days, value_attr="total")
    sharpe = calc.sharpe_ratio(value_days, value_attr="total")
    portfolio.data["metadata"][str(portfolio.date)] = {
        "total_value": metadata.total_value(portfolio),
        "cagr": cagr,
        "max_draw_down": mdd,
        "sharpe_ratio": sharpe,
    }


def get_metadata(portfolio: models.Portfolio) -> dict:
    """Get the metadata at the current data for the portfolio - calculate if needed"""
    if portfolio.date not in portfolio.data["metadata"]:
        set_metadata(portfolio)
    return portfolio.data["metadata"][str(portfolio.date)]


def get_portfolio(name: str, detailed: bool = False) -> dict:
    """Get a specific portfolio
    When detailed=True, metadata and strategy data are fetched, computed if needed
    """
    query = select(models.Portfolio).where(models.Portfolio.name == name)
    session = db.get_session()
    session.expire_on_commit = False
    result = session.execute(query).one()
    portfolio = result[0]
    if detailed:
        portfolio.data["metadata"][str(portfolio.date)] = get_metadata(portfolio)
    return portfolio


def update_portfolio(portfolio: models.Portfolio):
    """Save a portfolio"""
    # SQLAlchemy doesn't notice that JSON fields change unless you flag_modified
    flag_modified(portfolio, "data")
    db.commit(portfolio)


def list_portfolios(detailed: bool = False):
    """Return a list of all portfolios"""
    query = select(models.Portfolio)
    session = db.get_session()
    result = session.execute(query).all()
    portfolios = [res[0] for res in result]
    detailed_portfolios = []
    if detailed:
        for portfolio in portfolios:
            detailed_portfolio = get_portfolio(portfolio.name, detailed=True)
            detailed_portfolios.append(detailed_portfolio)
        return detailed_portfolios
    else:
        return portfolios


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
