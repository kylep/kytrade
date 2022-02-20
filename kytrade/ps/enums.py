"""ps enums"""
from enum import Enum


class TransactionAction(Enum):
    """Buy or sell transactions"""

    BUY = "BUY"
    SELL = "SELL"


class CashOperationAction(Enum):
    """Buy or sell transactions"""

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
