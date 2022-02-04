"""Alpaca API"""
import requests
from kytrade.const import ALPACA_API_KEY_ID, ALPACA_API_KEY_SECRET, ALPACA_API_ENDPOINT


HEADERS = {"APCA-API-KEY-ID": ALPACA_API_KEY_ID, "APCA-API-SECRET-KEY": ALPACA_API_KEY_SECRET}


def account_data():
    """Get the account data"""
    url = f"{ALPACA_API_ENDPOINT}/v2/account"
    return requests.get(url, headers=HEADERS).json()


def get_historical_data(
    ticker: str, limit=10000, adjustment="all", start=None, end=None, page_token=None
):
    """Get historical data
    max limit: 10000
    adjustment: raw, split, dividend, all
    start: RFC-3339 format string
    end: RFC-3339 format string
    page_token: used for recursive paginated queries
    """
    raise NotImplementedError("This returns 404s for some reason")  # fix or remove...
    opt_parms = []
    if start:
        opt_parms.append(f"start={start}")
    if end:
        opt_parms.append(f"end={end}")
    if page_token:
        opt_parms.append(f"page_token={page_token}")
    url = "&".join(
        [
            f"{ALPACA_API_ENDPOINT}/v2/stocks/{ticker}/bars?",
            "timeframe=1Day",
            f"limit={limit}",
            f"adjustment={adjustment}",
        ]
        + opt_parms
    )
    return requests.get(url, headers=HEADERS).json()
