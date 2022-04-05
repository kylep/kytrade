"""IEXcloud
IEX Cloud includes up to 15 years of historical end-of-day price, but only if you pay them.
For free accounts, you only get 5 years.

Minute-by-minute price data exists for the last 30 days.

They charge using a credit system, with the free account having a certain low qty of credits
"""
# pylint: skip-file
import requests
from kytrade.const import IEXCLOUD_API_KEY


SANDBOX_URL = "https://sandbox.iexapis.com/stable"
BASE_URL = "https://cloud.iexapis.com/stable"


class FuckYouPayMeError(Exception):
    """This feature isn't supported for free users"""


def get_daily_history(ticker: str):
    """Query the daily history of a stock"""
    url = f"{BASE_URL}/...?token={IEXCLOUD_API_KEY}"


def balance_sheet():
    return "/stock/{symbol}/balance-sheet/{last}/{field}"


def quote(ticker: str):
    url = f"{BASE_URL}/stock/{ticker}/quote?token={IEXCLOUD_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 402:
        raise FuckYouPayMeError(f"iex.quote: {resp.content.decode('ascii')}")
    return resp.json()


def financials(ticker: str):
    """get yearly fiancials"""
    url = f"{BASE_URL}/stock/{ticker}/financials?token={IEXCLOUD_API_KEY}&period=annual"
    resp = requests.get(url)
    if resp.status_code == 402:
        raise FuckYouPayMeError(f"iex.financials: {resp.content.decode('ascii')}")
    return resp
