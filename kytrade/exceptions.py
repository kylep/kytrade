"""Exceptions"""


class InsufficientFundsError(Exception):
    """Cash balance is too low to buy"""


class InsufficientSharesError(Exception):
    """Can't remove shares you don't have"""


class InvalidStrategyConditionName(Exception):
    """The provided strategy condition name does not exist"""


class InvalidStrategyActionName(Exception):
    """The provided strategy action name does not exist"""
