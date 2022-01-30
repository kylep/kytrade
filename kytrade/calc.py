"""Calculations - Easier to test here than in the portfolio"""
import math


def compound_anual_growth_rate(begin_value: float, end_value: float, years: float) -> float:
    """Return the CAGR of given values"""
    # https://www.investopedia.com/terms/c/cagr.asp
    if begin_value == 0 or years == 0:
        return 0
    return ((end_value / begin_value) ** (1 / years) - 1) * 100


def average(values: list):
    """Return the average"""
    return sum(values) / len(values)


def variance(values: list, degrees_of_freedom: int = 1) -> float:
    """Given a list of stock prices, calculate their daily variance"""
    num_values = len(values)
    mean = average(values)
    return sum([(value - mean) ** 2 for value in values]) / (num_values - degrees_of_freedom)


def standard_deviation(values: list, degrees_of_freedom: int = 1) -> float:
    """Return the standard deviation at close of given stocks"""
    return math.sqrt(variance(values, degrees_of_freedom=degrees_of_freedom))


def bollinger_bands(values: list) -> dict:
    """Return a dict with keys high,low,sma"""
    sma = average(values)
    bband_size = standard_deviation(values) * 2
    high = sma + bband_size
    low = sma - bband_size
    return {"high": high, "low": low, "sma": sma}
