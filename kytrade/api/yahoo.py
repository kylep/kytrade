"""Yahoo Finance
limited to 2,000 requests per hour per IP, 48,000 requests a day
"""
import datetime
import yfinance

from kytrade.data.models import DailyStockPrice


def get_daily_stock_history(symbol: str) -> list:
    """Use yahoo finance to download daily stock data"""
    start = datetime.datetime(1900, 1, 1)
    end = datetime.date.today()
    daily_stock_prices = []
    df = yfinance.download(symbol, start=start, end=end, progress=False)
    stocks = df.reset_index().to_dict("records")
    for stock in stocks:
        daily_stock_price = DailyStockPrice(
            ticker=symbol,
            date=stock["Date"].to_pydatetime().date(),
            open=stock["Open"],
            close=stock["Close"],
            high=stock["High"],
            low=stock["Low"],
            volume=stock["Volume"],
        )
        daily_stock_prices.append(daily_stock_price)
    return daily_stock_prices
