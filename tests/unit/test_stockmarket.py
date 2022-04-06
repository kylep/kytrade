"""Test the stock market simulator"""

from kytrade import stockmarket


def test_stock_market_constructor():
    """Instiantiate a StockMarket"""
    market = stockmarket.StockMarket()
