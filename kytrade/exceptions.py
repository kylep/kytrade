"""Exceptions"""


class InsufficientFundsError(Exception):
    """Cash balance is too low to buy"""


class InsufficientSharesError(Exception):
    """Can't remove shares you don't have"""


class InvalidStrategyConditionName(Exception):
    """The provided strategy condition name does not exist"""


class InvalidStrategyActionName(Exception):
    """The provided strategy action name does not exist"""


class InvalidTotalPortfolioAllocationPercentage(Exception):
    """The sum given percentage args in action (ex. rebalance) are not as expected (usually 100)"""
