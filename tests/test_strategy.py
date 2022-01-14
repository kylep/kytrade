"""strategy tests"""
from kytrade.strategy.strategy import BaseDailyStrategy
from kytrade.portfolio import Portfolio

def test_BaseDailyStrategy():
    portfolio = Portfolio(date="2020-02-02", balance=900.12)
    strat = BaseDailyStrategy(portfolio)
    assert strat
