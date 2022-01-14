""" test kytrade.portfolio """
from kytrade.portfolio import Portfolio, SharePosition

def test_share_position_init():
    sp = SharePosition(ticker="AAPL")

def test_portfolio_init():
    portfolio = Portfolio(date="2020-02-02", balance=100.23)
