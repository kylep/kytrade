""" test kytrade.portfolio_simulator """
import pytest
import datetime
import kytrade.portfolio_simulator as portfolio_simulator
from kytrade.data import models


@pytest.fixture
def mock_session(mocker):
    """SQLA PortfolioSim session()"""
    m_session = mocker.MagicMock(name="m_session")
    m_session.return_value.execute.return_value.all.return_value = []
    mocker.patch("kytrade.portfolio_simulator.get_session", m_session)


@pytest.fixture
def mock_daily_stock_price(mocker):
    """kytrade.data.daily_stock_price"""
    m_dsp = mocker.MagicMock(name="m_dsp")
    m_dsp.fetch.return_value = [
        models.DailyStockPrice(
            id=1,
            date="1900-01-01",
            ticker="FOO",
            open=10.12,
            close=12.34,
            high=14.14,
            low=9.23,
            volume=9001,
        )
    ]
    mocker.patch("kytrade.portfolio_simulator.daily_stock_price", m_dsp)


def test_portfolio_constructor(mock_session):
    """constructor"""
    assert portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")


def test_portfolio_days(mock_session):
    """test advancing the days in the portfolio"""
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    assert isinstance(portsim.orm_ps.date, datetime.date)
    init_date = portsim.orm_ps.date
    portsim.advance_one_day()
    assert init_date != portsim.orm_ps.date
    assert str(portsim.orm_ps.date) == "2000-01-02"
    portsim.advance_to_date("2000-03-03")
    assert str(portsim.orm_ps.date) == "2000-03-03"


def test_portfolio_balance(mock_session):
    """test moving money around"""
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    assert portsim.balance == 0
    test_val = 1000.99
    portsim.balance = test_val  # call the setter
    assert portsim.balance == test_val
    assert portsim.orm_ps.usd == test_val
    with pytest.raises(portfolio_simulator.InsufficientFundsError):
        portsim.balance -= 9999


def test_portfolio_stock_positions(mock_session):
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    # check empty position list
    assert isinstance(portsim.stock_positions, list)
    assert len(portsim.stock_positions) == 0
    # try and remove some shares from empty list
    with pytest.raises(portfolio_simulator.InsufficientSharesError):
        portsim.remove_stock("FOO", 5)
    # add some shares (free)
    portsim.add_stock("FOO", 3)
    assert len(portsim.stock_positions) == 1
    assert portsim.stock_positions[0].ticker == "FOO"
    assert portsim.stock_positions[0].qty == 3
    # add more shares
    portsim.add_stock("FOO", 3)
    assert portsim.stock_positions[0].qty == 6
    # remove some shares
    portsim.remove_stock("FOO", 5)
    assert portsim.stock_positions[0].qty == 1
    # try and remove more shares than you have
    with pytest.raises(portfolio_simulator.InsufficientSharesError):
        portsim.remove_stock("FOO", 5)

def test_portfolio_buy_sell_stock(mock_session, mock_daily_stock_price):
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    # buy some shares with no money
    with pytest.raises(portfolio_simulator.InsufficientFundsError):
        portsim.buy_stock(ticker="FOO", qty=10, at="open")  # mocked from mock_daily_stock_price
    assert not portsim.stock_positions
    # buy shares with some money
    balance = 9999.99
    portsim.balance = balance
    portsim.buy_stock(ticker="FOO", qty=10, at="open")  # mocked from mock_daily_stock_price
    assert portsim.stock_positions
    assert len(portsim.stock_positions) == 1
    assert portsim.stock_positions[0].ticker == "FOO"
    assert portsim.stock_positions[0].qty == 10


