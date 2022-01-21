import datetime
from sqlalchemy import select, delete, desc, or_
from sqlalchemy.exc import NoResultFound

from kytrade.data.db import get_session
from kytrade.data import models
from kytrade.data import daily_stock_price


class InsufficientFundsError(Exception):
    """Balance is too low to buy"""


class InsufficientSharesError(Exception):
    """Can't remove shares you don't have"""


class Portfolio:
    """Portfolio Simulator"""

    def __init__(self, name: str, date: str):
        """Instantiate a new Portfolio Simulator instance"""
        ps = models.PortfolioSimulator()
        ps.name = name
        ps.date = datetime.date.fromisoformat(str(date))
        ps.usd = 0
        ps.opened = ps.date
        self.session = get_session()
        self.orm_ps = ps  # The DB portfolio_simulators row in ObjectRelationalModel format
        self.orm_stock_positions = []  # list of PortSimStockPosition objects
        self.orm_stock_transactions = []  # list of PortSimStockTransaction objects
        self.orm_cash_operations = []  # list of PortSimCashOperation objects
        self.ps_balance_history = []  # list of PortfolioSimulatorBalanceHistoryDay objects
        self.on_open = []  # list of Strategy's to execute on market open
        self.on_close = []  # ...to execute on market close

    @staticmethod
    def load(name_or_id):
        """Load a Portfolio gtom the db by id and return its portfolio simulator object"""
        session = get_session()
        query = select(models.PortfolioSimulator).where(
            or_(
                models.PortfolioSimulator.id == name_or_id,
                models.PortfolioSimulator.name == name_or_id,
            )
        )
        orm_ps = session.execute(query).one()[0]
        instance = Portfolio(orm_ps.name, orm_ps.date)
        instance.session = session  # Otherwise the orm_object is bound to the wrong session
        instance.orm_ps = orm_ps
        return instance

    @property
    def balance(self):
        """in usd"""
        return self.orm_ps.usd

    @balance.setter
    def balance(self, value):
        """Set the portfolio balance - raise InsufficientFundsError if negative"""
        # Reminder: When implementing logging, log changes to balance
        delta = value - self.orm_ps.usd  # have 100, set value to 110, detla is +10
        if delta == 0:
            return  # no op
        action = "DEPOSIT" if delta > 0 else "WITHDRAW"
        cash_operation = models.PortSimCashOperation(
            portfolio_id=self.id, date=self.date, action=action, usd=value
        )
        self.orm_cash_operations.append(cash_operation)
        self.orm_ps.usd = value
        if value < 0:
            raise InsufficientFundsError(f"Portfolio balance {value} is negative")

    @property
    def current_value(self) -> float:
        """Current sum value of all stocks + balance"""

    @property
    def profit(self) -> float:
        """current sum value of all stocks + balance - deposited funds"""

    @property
    def date(self):
        """Get the Portfolio date from the orm"""
        return self.orm_ps.date

    @property
    def name(self):
        """Get the Portfolio from the orm"""
        return self.orm_ps.name

    @property
    def id(self):
        """Get the portfolio ID - save the portfolio first to generate it if needed"""
        if self.orm_ps.id:
            return self.orm_ps.id
        self.session.add(self.orm_ps)
        self.session.commit()
        self.session.refreshself.orm_ps()
        if not self.orm_ps.id:
            # This should never happen, unless...
            raise Exception("Failed to get ID for portfolio - is auto-increment broken?")
        return self.orm_ps.id

    @property
    def stock_positions(self):
        """Get the stock positions - read from DB on first query"""
        if not self.orm_stock_positions:
            query = select(models.PortSimStockPosition).where(
                models.PortSimStockPosition.portfolio_id == self.id
            )
            positions = self.session.execute(query).all()  # returns a list of tupples (<data>,)
            self.orm_stock_positions = [pos[0] for pos in positions]  # de-tuppling
        return self.orm_stock_positions

    @property
    def stock_transactions(self):
        """List of PortSimStockTransaction orm objects"""
        if not self.orm_stock_transactions:
            # Note: I had been using position_id here and not saving the ticker in the transactions
            # but the ID wasn't getting generated in time to be useful. If I used UUIDs that would
            # fix this problem, or I could just save json strings with each portfolio
            # ...thinking on it
            query = select(models.PortSimStockTransaction).where(
                models.PortSimStockTransaction.portfolio_id == self.id
            )
            transactions = self.session.execute(query).all()
            transactions = [tx[0] for tx in transactions]  # de-tuppling
            self.orm_stock_transactions += transactions
        return self.orm_stock_transactions

    @property
    def tx_profit(self):
        """Profit from all the transactions so far + the value of current positions"""
        tx_profit = 0
        for transaction in self.stock_transactions:
            multiplier = 1 if transaction.action == "SELL" else -1  # buy subtracts, sell adds $
            tx_profit += multiplier * transaction.qty * transaction.unit_price
        return tx_profit

    def advance_one_day(self):
        """Advance one day"""
        self.orm_ps.date += datetime.timedelta(days=1)

    def advance_to_date(self, date: str = None):
        """Advance the date one day, or to the given date YYYY-MM-DD"""
        dt_date = datetime.date.fromisoformat(date)
        while self.orm_ps.date < dt_date:
            self.advance_one_day()

    def add_stock(self, ticker, qty):
        """Add shares, creating a new position if needed"""
        position = next((pos for pos in self.stock_positions if pos.ticker == ticker), None)
        if not position:
            position = models.PortSimStockPosition(portfolio_id=self.id, ticker=ticker, qty=0)
            self.orm_stock_positions.append(position)
        position.qty += qty

    def remove_stock(self, ticker, qty):
        """Remove shares, but keep the position option with 0 qty

        Raise InsufficientSharesError if not enough shares exist
        """
        position = next((pos for pos in self.stock_positions if pos.ticker == ticker), None)
        current_qty = position.qty if position else 0
        new_qty = current_qty - qty
        if not position or new_qty < 0:
            raise InsufficientSharesError(f"Can't remove {qty} x {ticker}: have {current_qty}")
        position.qty = new_qty

    def log_transaction(self, ticker: str, qty: int, unit_price: float, action: str):
        """Add a stock transaction to this portfolio's stock transaction log
        action: BUY or SELL
        """
        transaction = models.PortSimStockTransaction(
            portfolio_id=self.id,
            ticker=ticker,
            date=self.date,
            qty=qty,
            unit_price=unit_price,
            action=action,
        )
        self.orm_stock_transactions.append(transaction)

    def buy_stock(self, ticker: str, qty: int, at: str, price=None, comp=False):
        """Add shares and subtract the cost from the balance - exception if overdrawn
        at: open, close, price
        price: used instead of open/close when at:price is specified
        comp: complimentary - add the price to balance before buying
        """
        dsp = daily_stock_price.fetch(ticker, from_date=self.date, limit=1)[0]
        price = price if price else getattr(dsp, at)
        total_price = price * qty
        if comp:
            self.balance += total_price
        self.balance -= total_price
        self.add_stock(ticker, qty)
        self.log_transaction(ticker=ticker, qty=qty, unit_price=price, action="BUY")

    def sell_stock(self, ticker: str, qty: int, at: str, price=None):
        """Sell shares and add the total to the balance - exception if shares are not owned
        at: open, close, price
        price: used instead of open/close when at:price is specified
        """
        dsp = daily_stock_price.fetch(ticker, from_date=self.date, limit=1)[0]
        price = price if price else getattr(dsp, at)
        self.remove_stock(ticker, qty)
        self.balance += price * qty
        self.log_transaction(ticker=ticker, qty=qty, unit_price=price, action="SELL")

    def save(self):
        """Save this portfolio instance to the database"""
        # Save the ps
        self.session.add(self.orm_ps)
        self.session.commit()
        self.session.refresh(self.orm_ps)  # Refresh the portfolio ID
        # Save each transaction - make sure they link to this portfolio
        # TODO: change the tx schema to track ticker and portfolio ID instead of position ID
        for record in (
            self.orm_stock_positions + self.orm_stock_transactions + self.orm_cash_operations
        ):
            record.portfolio_id = self.id  # TODO: I don't think I need this any more...
            self.session.add(record)
        self.session.commit()

    def delete(self):
        """Delete this portfolio simulator instance"""
        # don't forget self.ps_balance_history once implemented
        for stock_transaction in self.orm_stock_transactions:
            self.session.delete(stock_transaction)
        for stock_position in self.orm_stock_positions:
            self.session.delete(stock_position)
        self.session.delete(self.orm_ps)
        self.session.commit()


def list_portfolios() -> list:
    """List all portfolio_sims decending by date"""
    query = select(models.PortfolioSimulator).order_by(desc(models.PortfolioSimulator.date))
    ps_orm_list = [elem[0] for elem in get_session().execute(query).all()]
    return [Portfolio.load(sim.id) for sim in ps_orm_list]
