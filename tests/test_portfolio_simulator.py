""" test kytrade.portfolio_simulator """
import pytest
import datetime
import kytrade.ps.portfolio as portfolio_simulator
from kytrade.data import models
from kytrade.stock_market import SpotPrice

@pytest.fixture
def mock_session(mocker):
    """SQLA PortfolioSim session()"""
    m_session = mocker.MagicMock(name="m_session")
    m_session.return_value.execute.return_value.all.return_value = []
    mocker.patch("kytrade.portfolio_simulator.get_session", m_session)


@pytest.fixture
def mock_stock_market_daily_price(mocker):
    """kytrade.stock_market"""
    m_dsp = mocker.MagicMock(name="m_dsp")
    m_dsp.return_value.get_daily_price.return_value = [
        models.DailyStockPrice(
            id=1,
            date="1999-01-01",
            ticker="FOO",
            open=100.11,
            close=200.22,
            high=300.33,
            low=10.10,
            volume=9001,
        )
    ]
    m_dsp.return_value.get_spot.return_value = SpotPrice(100.11, 200.22)
    mocker.patch("kytrade.portfolio_simulator.StockMarket", m_dsp)



