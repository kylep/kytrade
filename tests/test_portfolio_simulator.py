""" test kytrade.portfolio_simulator """
import pytest
import datetime
import kytrade.portfolio_simulator as portfolio_simulator
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


def test_portfolio_value(mock_session):
    """test moving money around"""
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    assert portsim.cash == 0
    test_val = 1000.99
    portsim.cash = test_val  # call the setter
    assert portsim.cash == test_val
    assert portsim.orm_ps.usd == test_val
    with pytest.raises(portfolio_simulator.InsufficientFundsError):
        portsim.cash -= 9999


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


def test_portfolio_buy_sell_stock(mock_session, mock_stock_market_daily_price):
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    # buy some shares with no money
    with pytest.raises(portfolio_simulator.InsufficientFundsError):
        portsim.buy_stock(
            ticker="FOO", qty=10, at="open"
        )  # mocked from mock_stock_market_daily_price
    assert not portsim.stock_positions
    assert not portsim.stock_transactions
    # buy shares with some money
    start_cash = 9999.99
    buy_qty = 10
    portsim.cash = start_cash
    portsim.buy_stock(
        ticker="FOO", qty=buy_qty, at="open"
    )  # mocked from mock_stock_market_daily_price
    # a stock_position and stock_transaction should be created
    assert portsim.stock_positions
    assert len(portsim.stock_positions) == 1
    assert len(portsim.stock_transactions) == 1
    # the stock_position should hold the ticker and quantity, and the cash should be lower
    assert portsim.stock_positions[0].ticker == "FOO"
    assert portsim.stock_positions[0].qty == buy_qty
    assert portsim.cash < start_cash
    # the cash should be the starting cash minus the transaction cost
    unit_price = portsim.stock_transactions[0].unit_price
    new_cash = start_cash - (unit_price * buy_qty)
    assert portsim.cash == new_cash
    # the transaction should show that it was a BUY and link to the id of the stock position
    assert portsim.stock_transactions[0].action == "BUY"
    assert portsim.stock_transactions[0].portfolio_id == portsim.id
    assert portsim.stock_transactions[0].ticker == "FOO"
    portsim.buy_stock(
        ticker="FOO", qty=buy_qty, at="open"
    )  # mocked from mock_stock_market_daily_price
    # new stock positions should only be made for new shares
    assert len(portsim.stock_positions) == 1
    # new transactions made for each buy
    assert len(portsim.stock_transactions) == 2
    # list ordering is ok
    assert portsim.stock_transactions[1].portfolio_id == portsim.id
    with pytest.raises(portfolio_simulator.InsufficientFundsError):
        portsim.buy_stock(
            ticker="FOO", qty=9999, at="open"
        )  # mocked from mock_stock_market_daily_price
    with pytest.raises(portfolio_simulator.InsufficientSharesError):
        portsim.sell_stock("FOO", 9999, at="close")


def test_deposit_withdraw(mock_session):
    portsim = portfolio_simulator.Portfolio(name="TEST", date="2000-01-01")
    assert len(portsim.orm_cash_operations) == 0
    # deposit cash
    deposit = 500.50
    portsim.deposit(deposit)
    assert len(portsim.orm_cash_operations) == 1
    assert portsim.orm_cash_operations[0].usd == deposit
    assert portsim.orm_cash_operations[0].action == "DEPOSIT"
    assert portsim.orm_cash_operations[0].portfolio_id == portsim.id
    assert portsim.cash == deposit
    # withdraw cash
    withdraw = 100.50
    portsim.withdraw(withdraw)
    assert len(portsim.orm_cash_operations) == 2
    assert portsim.orm_cash_operations[1].usd == withdraw
    assert portsim.orm_cash_operations[1].action == "WITHDRAW"
    assert portsim.cash == deposit - withdraw
