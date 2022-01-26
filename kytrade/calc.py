"""Calculations - Easier to test here than in the portfolio"""


def compound_anual_growth_rate(begin_value: float, end_value: float, years: int) -> float:
    """Return the CAGR of given values"""
    # https://www.investopedia.com/terms/c/cagr.asp
    if begin_value == 0:
        return 0
    return ((end_value / begin_value)**(1 / years) - 1) * 100

