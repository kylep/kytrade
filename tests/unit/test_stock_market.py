"""Test the stock market simulator"""

from kytrade import stock_market


def test_stock_market_constructor():
    """Instiantiate a StockMarket"""
    market = stock_market.StockMarket()
