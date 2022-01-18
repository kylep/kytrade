""" test kytrade.portfolio_simulator """
import pytest
import datetime
import kytrade.portfolio_simulator as portfolio_simulator


@pytest.fixture
def mock_session(mocker):
    """SQLA PortfolioSim session()"""
    mocker.patch("kytrade.portfolio_simulator.get_session")


def test_portfolio_constructpr(mock_session):
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
