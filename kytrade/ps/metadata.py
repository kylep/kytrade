"""Derived portfolio data - metadata"""
from kytrade.data import models
from kytrade.stock_market import StockMarket
from kytrade.ps.enums import CashOperationAction


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
