"""Derived portfolio data - metadata"""
import datetime
from collections import namedtuple

from kytrade.data import models
from kytrade.stockmarket import StockMarket
from kytrade.ps.enums import CashOperationAction


def value_days_history_named_tuples(portfolio: models.Portfolio) -> list:
    """Return a list of ValueDay tupple objects representing the value history"""
    days = []
    # This named tupple is used for consistency with the StockMarket days entries
    ValueDay = namedtuple("ValueDay", "date total")
    for date, data in portfolio.data["value_history"].items():
        date_dt = datetime.date.fromisoformat(date)
        days.append(ValueDay(date_dt, data["total_usd"]))
    return days


def total_value(portfolio: models.Portfolio) -> float:
    """Return the value of all stocks + cash in given portfolio"""
    sm = StockMarket()
    total = portfolio.data["cash"]
    for symbol in portfolio.data["stock_positions"]:
        qty = portfolio.data["stock_positions"][symbol]
        unit_price = sm.get_spot(symbol, portfolio.date).close
        total += qty * unit_price
    return total


def total_deposited(portfolio: models.Portfolio) -> float:
    """Return the sum of all deposits"""
    total = 0
    for cash_operation in portfolio.data["cash_operations"]:
        if CashOperationAction(cash_operation["action"]) == CashOperationAction.DEPOSIT:
            total += cash_operation["usd"]
    return total


def total_withdrawn(portfolio: models.Portfolio) -> float:
    """Return the sum of all withdrawls"""
    total = 0
    for cash_operation in portfolio.data["cash_operations"]:
        if CashOperationAction(cash_operation["action"]) == CashOperationAction.WITHDRAW:
            total += cash_operation["usd"]
    return total


def profit(portfolio: models.Portfolio) -> float:
    """Return the total_value plus total withdrawn minus total deposited"""
    return total_value(portfolio) + total_withdrawn(portfolio) - total_withdrawn(portfolio)


def sorted_stock_position_values(portfolio: models.Portfolio) -> list:
    """Return a list of {"symbol": "", value: #} sorted by value"""
    positions = portfolio.data["stock_positions"]
    sm = StockMarket()
    ret = []
    for symbol in positions:
        qty = positions[symbol]
        unit_price = sm.get_spot(symbol, portfolio.date).close
        value = qty * unit_price
        ret.append({"symbol": symbol, "value": value})
    return sorted(ret, key=lambda k: k["value"])
