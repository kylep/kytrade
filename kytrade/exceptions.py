"""Exceptions"""

class InsufficientFundsError(Exception):
    """Cash balance is too low to buy"""


class InsufficientSharesError(Exception):
    """Can't remove shares you don't have"""
