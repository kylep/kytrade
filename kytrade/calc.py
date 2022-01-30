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
    status = "INSIDE"
    if values[0] > high:
        status = "ABOVE"
    elif values[0] < low:
        status = "BELOW"
    return {"high": high, "low": low, "sma": sma, "status": status}


def max_drawdown(values: list) -> dict:
    """Calculate the max drawdown (MDD) of given chronologically descending ordered list
    To use MDD as a percentage, multiply ratio by -100
    Return dict with keys: peak, trough, ratio, absolute
    """
    ret = {"peak": 0, "trough": 0, "ratio": 0, "absolute": 0}
    mdd = 0
    for i, value in reversed(list(enumerate(values))):
        peak = max(values[: i + 1])  # not efficient!
        trough = min(values[i:])  # also maybe not efficient!
        test_mdd = (trough - peak) / peak
        if test_mdd < mdd:
            mdd = test_mdd
            ret = {
                "peak": peak,
                "trough": trough,
                "ratio": mdd,
                "percent": (mdd * -100),
                "absolute": (peak - trough),
            }
    return ret
