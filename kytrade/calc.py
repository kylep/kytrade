"""Metadata Calculations"""
import math

import pandas

from kytrade import const

# Reminder: To step through these functions, drop step_trace at the end of an interation
# import pdb  # pdb.set_trace()


def copy_and_conditionally_reverse_days(days: list, old_to_new=True) -> list:
    """Return a copy of the days list - reverses it if the order is wrong"""
    new_days = days.copy()
    if not new_days or len(new_days) < 2:
        return new_days
    if (days[0].date > days[1].date and old_to_new) or (
        days[0].date < days[1].date and not old_to_new
    ):
        new_days.reverse()
    return new_days


def compound_anual_growth_rate(days: list, value_attr: str) -> float:
    """Return the CAGR computed from given descending-dated days"""
    # https://www.investopedia.com/terms/c/cagr.asp
    if not days:
        return 0
    years = (days[0].date - days[-1].date).days / 365.25
    years = round(years, 2)  # floating point math problems
    begin_value = getattr(days[-1], value_attr)
    end_value = getattr(days[0], value_attr)
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


def indexed_min(values: list) -> tuple:
    """Return tupple (min value, list index)
    Using the .index() approach after min() can return the wrong index when there're duplicates
    """
    minval = (values[0], 0)
    for i, value in enumerate(values):
        if value < minval[0]:
            minval = (value, i)
    return minval


def indexed_max(values: list) -> tuple:
    """Return tupple (max value, list index)
    Using the .index() approach after max() can return the wrong index when there're duplicates
    """
    maxval = (values[0], 0)
    for i, value in enumerate(values):
        if value > maxval[0]:
            maxval = (value, i)
    return maxval


def max_drawdown(days: list, value_attr: str) -> dict:
    """Calculate the max drawdown (MDD) of given chronologically descending ordered list of days
    Return dict with keys: peak, peak_date, trough, trough_date, ratio, absolute
    """
    # This approach is a bit harder to read but lowers the average compute time from ~ 15.5 to 2.5s
    if not days:
        return {
            "peak": 0,
            "peak_date": "",
            "trough": 0,
            "trough_date": "",
            "ratio": 0,
            "percent": 0,
            "absolute": 0,
        }
    ret = None
    days = copy_and_conditionally_reverse_days(days, old_to_new=True)
    values = [getattr(day, value_attr) for day in days]  # (list order is preserved)
    index = 0
    peak = values[0]
    peak_date = days[index].date
    trough, trough_index = indexed_min(values)
    trough_date = days[trough_index].date
    for index in range(len(values)):
        # if the new peak is higher than the old peak, raise the peak
        if values[index] > peak:
            peak = values[index]
            peak_date = days[index].date
        # if the index is higher than the previous trough_index, that trough now longer applies, so
        # we need to find a new one in the future of the current index
        future_values = values[index:]
        new_trough, new_trough_index = indexed_min(future_values)
        if new_trough < trough or index > trough_index:
            trough = new_trough
            trough_index = new_trough_index + index  # trough_index is offset from today
            trough_date = days[trough_index].date
        # calculate the new mdd and save it if it's lower as the return value
        ratio = 0 if peak == 0 else (trough - peak) / peak
        mdd = {
            "peak": peak,
            "peak_date": peak_date,
            "trough": trough,
            "trough_date": trough_date,
            "ratio": ratio,
            "percent": (ratio * -100),
            "absolute": (peak - trough),
        }
        if not ret or mdd["ratio"] < ret["ratio"]:
            ret = mdd
    assert peak_date < trough_date  # This keeps happening...
    return ret


def get_metadata(days: list, value_attr: str):
    """Return a dict of metadata about this series of days
    Days are expected to be in reverse chronological order - index 0 is the latest data - stack
    The value attribute is the one to be computed, such as "close" from daily stock prices
    """
    values = [getattr(day, value_attr) for day in days]  # preserves order
    return {
        "count": len(days),
        "start": str(days[-1].date),
        "end": str(days[0].date),
        "compound_anual_growth_rate": compound_anual_growth_rate(days, value_attr),
        "last_value": values[0],
        "high": max([day.high for day in days]),
        "low": min([day.low for day in days]),
        "20_day_average": average(values[:20]),
        "200_day_average": average(values[:200]),
        "all_time_average": average(values),
        "20_day_variance": variance(values[:20]),
        "200_day_variance": variance(values[:200]),
        "all_time_variance": variance(values),
        "20_day_standard_deviation": standard_deviation(values[:20]),
        "200_day_standard_deviation": standard_deviation(values[:200]),
        "all_time_standard_deviation": standard_deviation(values),
        "20d_bollinger_band": bollinger_bands(values[:20]),
        "max_drawdown": max_drawdown(days, value_attr),
    }


def sharpe_ratio(days: list, value_attr: str) -> float:
    """I'm not sure if this is right..."""
    if not days:
        return 0
    values = [getattr(day, value_attr) for day in days]
    cagr = compound_anual_growth_rate(days, value_attr)
    anualized_std_dev = standard_deviation(values) / len(days)
    return (cagr - const.RISK_FREE_RATE) / anualized_std_dev


def ___get_dicts_of_days_with_percent_change(days: list, value_attr: str) -> list:
    """Return [{"date": datetime.date, "value": <#>, "percent": <#>}] where percent is the
    change from one point to the next
    """
    days_pct = []
    for i, day in enumerate(days):
        if i == 0:
            continue
        yesterday = day[i - 1]
        last_val = getattr(day, value_attr)
        val = getattr(yesterday, value_attr)
        percent = val / last_val - 1
        days_pct.append({"date": day.date, "value": val, "percent": percent})
    return days_pct


def ___other_sharpe_ratio(days: list, value_attr: str) -> float:
    """Calculate the sharpe ratio"""
    if len(days) == 0:
        return 0
    days = copy_and_conditionally_reverse_days(days, old_to_new=True)
    days_pct = get_dicts_of_days_with_percent_change(days, value_attr)
    days.remove(days[0])  # pop the top element off the list - had to remove it for days_pct too
    values = [getattr(day, value_attr) for day in days]
    std_dev = standard_deviation(values)
    avg_daily_pct
    # ...............
    days = days.copy()
    return_of_portfolio = compound_anual_growth_rate(days, value_attr)
    risk_free_rate = const.RISK_FREE_RATE
    # standard_deviation(values)
    # values = [getattr(day, value_attr) for days]
    # sharpe_ratio = (return_of_portfolio - risk_free_rate) / excess_return_standard_deviation
    # anualize by multiplying by the sqrt of the # of days
    # number_of_days = len(days)
    # anualized_sharpe = sharpe_ratio * math.sqrt(number_of_days)
