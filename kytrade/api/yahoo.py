"""Yahoo Finance
limited to 2,000 requests per hour per IP, 48,000 requests a day
"""
import datetime
import yfinance

from kytrade import const
from kytrade.data.models import DailyStockPrice


def get_daily_stock_history(symbol: str) -> list:
    """Use yahoo finance to download daily stock data"""
    start = datetime.datetime(1900, 1, 1)
    end = datetime.date.today()
    daily_stock_prices = []
    df = yfinance.download(symbol, start=start, end=end, progress=False)
    stocks = df.reset_index().to_dict("records")
    close_key = "Adj Close" if const.ADJUST_FOR_DIVIDENDS else "Close"
    for stock in stocks:
        # close options: "Close", "Adj Close"
        daily_stock_price = DailyStockPrice(
            ticker=symbol,
            date=stock["Date"].to_pydatetime().date(),
            open=stock["Open"],
            close=stock[close_key],
            high=stock["High"],
            low=stock["Low"],
            volume=stock["Volume"],
        )
        daily_stock_prices.append(daily_stock_price)
    return daily_stock_prices
