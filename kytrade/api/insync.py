"""IBKR TWS via ib_insync

You gotta pay IBKR for some market data for anything to work. Its like $15/mo, $5 if you spend
enough on their comissions. Seems very detailed and real-time-y but not a ton of history.
"""
from ib_insync import *


PROD_PORT = 7496
PAPER_PORT = 7497
READ_ONLY = True


def download_daily_stock_history(symbol: str, exchange="NYSE", currency="USD", client_id=1):
    """Download the historical data
    Sadly, only returns like 5 or 10 years of data - works, though!
    Returns data in a weird list of lists with maybe some duplicates at the end or smth ¯\_(ツ)_/¯
    """
    ib = IB()
    ib.connect('127.0.0.1', PAPER_PORT, clientId=client_id, readonly=READ_ONLY)
    contract = Stock(symbol, exchange, currency)
    datestamp = ''
    bars_list = []
    while True:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=datestamp,
            durationStr='1 Y',
            barSizeSetting='1 day',
            whatToShow='MIDPOINT',
            useRTH=True,
            formatDate=1)
        if not bars:
            break
        bars_list.append(bars)
        if bars[0].date == datestamp:
            break
        datestamp = bars[0].date
        print(datestamp)
    return bars_list
