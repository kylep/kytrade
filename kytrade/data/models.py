"""SQL Alchemy models"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, UniqueConstraint

# too-few-public-methods is not appropriate in ORM classes
# pylint: disable=too-few-public-methods


Base = declarative_base()


def _gen_repr(clazz):
    """Print a usable constructor as the model representation - helps with troubleshooting"""
    keys = [key for key in clazz.__dict__.keys() if not key.startswith("_")]
    val_str = ", ".join([f"{key}={getattr(clazz, key)!r}" for key in keys])
    return f"{clazz.__class__.__name__}({val_str})"


class DailyStockPrice(Base):
    """Daily price data"""
    __tablename__ = "daily_stock_prices"
    __table_args__ = (UniqueConstraint("ticker", "date", name='ticker_date'),)
    id = Column(Integer, primary_key=True)
    ticker = Column(String(8))
    date = Column(Date)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    def __repr__(self):
        return _gen_repr(self)


class DailySMA(Base):
    """Simple Moving Average"""
    __tablename__ = "daily_sma"
    id = Column(Integer, primary_key=True)
    ticker = Column(String(8))
    date = Column(Date)
    style = Column(String(16))
    days = Column(Integer)
    value = Column(Float)
    def __repr__(self):
        return _gen_repr(self)


class PortfolioSimulator(Base):
    """Portfilio Simulator"""
    __tablename__ = "portfolio_simulators"
    __table_args__ = (UniqueConstraint("name"),)
    id = Column(Integer, primary_key=True)
    name = Column(String(256), )
    opened = Column(Date)
    date = Column(Date)
    usd = Column(Float)
    def __repr__(self):
        return _gen_repr(self)


class PortSimCashOperation(Base):
    """Track depositing/withdrawing funds from the portfolio
       action: DEPOSIT/WITHDRAW
    """
    # Really gotta figure out enums at some point...
    __tablename__ = "portfolio_simulator_cash_operations"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer)
    date = Column(Date)
    action = Column(String(8))  # DEPOSIT or WITHDRAW
    usd = Column(Float)
    def __repr__(self):
        return _gen_repr(self)


class PortfolioSimulatorValueHistoryDay(Base):
    """Portfilio Simulator Balance on a given day"""
    __tablename__ = "portfolio_simulator_balance_history_days"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer)
    date = Column(Date)
    total_usd = Column(Float)
    profit_usd = Column(Float)
    def __repr__(self):
        return _gen_repr(self)


class PortSimStockPosition(Base):
    """Portfolio Simulator Stock Positions"""
    __tablename__ = "port_sim_stock_positions"
    __table_args__ = (UniqueConstraint("portfolio_id", "ticker", name='portfolio_ticker'),)
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer)
    qty = Column(Integer)
    ticker = Column(String(8))
    def __repr__(self):
        return _gen_repr(self)


class PortSimStockTransaction(Base):
    """Portfolio Simulator Stock Transaction
       action: "buy" or "sell"
    """
    __tablename__ = "port_sim_stock_transactions"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer)
    ticker = Column(String(8))
    date = Column(Date)
    qty = Column(Integer)
    unit_price = Column(Float)
    action = Column(String(4))  # "buy" / "sell"  - Consider using an enum... compatability issues?
    def __repr__(self):
        return _gen_repr(self)


