import datetime
from sqlalchemy import select, delete, desc, or_
from sqlalchemy.exc import NoResultFound

from kytrade.data.db import get_session
from kytrade.data import models
from kytrade.stock_market import StockMarket


class InsufficientFundsError(Exception):
    """Cash balance is too low to buy"""


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
        self.market = StockMarket()
        self.orm_ps = ps  # The DB portfolio_simulators row in ObjectRelationalModel format
        self.orm_stock_positions = []  # list of PortSimStockPosition objects
        self.orm_stock_transactions = []  # list of PortSimStockTransaction objects
        self.orm_cash_operations = []  # list of PortSimCashOperation objects
        self.orm_value_history = []  # list of PortfolioSimulatorBalanceHistoryDay objects
        self.on_open = []  # list of Strategy's to execute on market open
        self.on_close = []  # ...to execute on market close

    @staticmethod
    def load(name_or_id):
        """Load a Portfolio from the db by id and return its portfolio simulator object"""
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
    def orm_objects(self):
        """Return a list of all the ORM objects associated with this portsim"""
        return (
            self.orm_stock_positions
            + self.orm_stock_transactions
            + self.orm_cash_operations
            + self.orm_value_history
        )

    @property
    def cash(self):
        """in usd"""
        return self.orm_ps.usd

    @cash.setter
    def cash(self, value):
        """Set the portfolio cash - raise InsufficientFundsError if negative"""
        self.orm_ps.usd = value
        if value < 0:
            raise InsufficientFundsError(f"Portfolio cash {value} is negative")

    @property
    def value_at_close(self) -> float:
        """Current sum value of all stocks + cash at the end of the day"""
        cval = self.cash
        for position in self.stock_transactions:
            cval += position.qty * self.market.get_spot(position.ticker, self.date).close
        return cval

    @property
    def total_deposited(self):
        """Sum of all cash deposits"""
        return sum([op.usd for op in self.cash_operations if op.action == "DEPOSIT"])

    @property
    def total_withdrawn(self):
        """Sum of all cash withdrawls"""
        return sum([op.usd for op in self.cash_operations if op.action != "DEPOSIT"])

    @property
    def profit(self) -> float:
        """current dollar profit of this portfolio"""
        return self.value_at_close + self.total_withdrawn - self.total_deposited

    @property
    def profit_percent(self) -> float:
        """Get the profit as a % of investment"""
        return 0 if not self.total_deposited else self.profit / self.total_deposited * 100

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
        self.session.refresh(self.orm_ps)
        return self.orm_ps.id

    def _load_orm_prop(self, model, orm_list: list):
        """Populate the ORM properies of the given model associated with this portfolio"""
        if not orm_list:
            query = select(model).where(model.portfolio_id == self.id)
            rows = self.session.execute(query).all()  # returns a list of tupples (<data>,)
            # orm_list is passed by reference so this updates self.orm_<orm_list>
            orm_list += [row[0] for row in rows]  # de-tuppling
        return orm_list

    @property
    def stock_positions(self):
        """Get the stock positions - read from DB on first query"""
        return self._load_orm_prop(models.PortSimStockPosition, self.orm_stock_positions)

    @property
    def stock_transactions(self):
        """List of PortSimStockTransaction orm objects"""
        return self._load_orm_prop(models.PortSimStockTransaction, self.orm_stock_transactions)

    @property
    def cash_operations(self):
        """List of PortSimCashOperation objects"""
        return self._load_orm_prop(models.PortSimCashOperation, self.orm_cash_operations)

    @property
    def value_history(self):
        return self._load_orm_prop(models.PortfolioSimulatorValueHistoryDay, self.orm_value_history)

    @property
    def tx_profit(self):
        """Profit from all the transactions so far + the value of current positions"""
        tx_profit = 0
        for transaction in self.stock_transactions:
            multiplier = 1 if transaction.action == "SELL" else -1  # buy subtracts, sell adds $
            tx_profit += multiplier * transaction.qty * transaction.unit_price
        return tx_profit

    def deposit(self, value):
        """deposit cash into the portsim"""
        cash_operation = models.PortSimCashOperation(
            portfolio_id=self.id, date=self.date, action="DEPOSIT", usd=value
        )
        self.orm_cash_operations.append(cash_operation)
        self.cash += value

    def withdraw(self, value):
        """withdraw cash from the portsim"""
        cash_operation = models.PortSimCashOperation(
            portfolio_id=self.id, date=self.date, action="WITHDRAW", usd=value
        )
        self.orm_cash_operations.append(cash_operation)
        self.cash -= value

    def _update_value_history(self):
        """Save today's value to the database"""
        day = models.PortfolioSimulatorValueHistoryDay(
            portfolio_id=self.id,
            date=self.date,
            total_usd=self.value_at_close,
            profit_usd=self.profit,
        )
        self.orm_value_history.append(day)

    def advance_one_day(self, print_status=False):
        """Advance one day"""
        self._update_value_history()
        self.orm_ps.date += datetime.timedelta(days=1)
        if print_status:
            print(f"{self.date}: {self.profit_percent:.2f}%                 ", end = "\r")

    def advance_to_date(self, date: str = None, print_status: bool = False):
        """Advance the date one day, or to the given date YYYY-MM-DD"""
        dt_date = datetime.date.fromisoformat(date)
        while self.orm_ps.date < dt_date:
            self.advance_one_day(print_status)

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
        """Add shares and subtract the cost from available cash - exception if overdrawn
        at: open, close, price
        price: used instead of open/close when at:price is specified
        comp: complimentary - add the price to cash before buying
        """
        spot = self.market.get_spot(ticker, self.date)
        price = price if price else getattr(spot, at)
        total_price = price * qty
        if comp:
            self.deposit(total_price)
        self.cash -= total_price
        self.add_stock(ticker, qty)
        self.log_transaction(ticker=ticker, qty=qty, unit_price=price, action="BUY")

    def sell_stock(self, ticker: str, qty: int, at: str, price=None):
        """Sell shares and add the total to the cash - exception if shares are not owned
        at: open, close, price
        price: used instead of open/close when at:price is specified
        """
        dsp = self.market.get_daily_price(ticker=ticker, from_date=self.date, limit=1)[0]
        price = price if price else getattr(dsp, at)
        self.remove_stock(ticker, qty)
        self.cash += price * qty
        self.log_transaction(ticker=ticker, qty=qty, unit_price=price, action="SELL")

    def save(self):
        """Save this portfolio instance to the database
        According to https://stackoverflow.com/questions/3659142/bulk-insert-with-sqlalchemy-orm,
        the ORM in general is not exactly great for high-performance. Oops.
        """
        # Save the ps first, can't associate the other orm objects with it otherwise
        self.session.add(self.orm_ps)
        self.session.commit()
        self.session.refresh(self.orm_ps)  # Refresh the portfolio ID
        # Save each transaction - make sure they link to this portfolio
        for record in self.orm_objects:
            record.portfolio_id = self.id  # TODO: I don't think I need this any more...
        #    self.session.add(record)  # This was not performing well ...
        # If you don't commit after each bulk_save you get a StaleDataError
        self.session.bulk_save_objects(self.orm_stock_positions)
        self.session.commit()
        self.session.bulk_save_objects(self.orm_stock_transactions)
        self.session.commit()
        self.session.bulk_save_objects(self.orm_cash_operations)
        self.session.commit()
        self.session.bulk_save_objects(self.orm_value_history)
        self.session.commit()

    def delete(self):
        """Delete this portfolio simulator instance"""
        for record in self.orm_objects:
            self.session.delete(record)
        self.session.delete(self.orm_ps)
        self.session.commit()

    def __repr__(self):
        """Print representation of this object"""
        return f"{self.__class__.__name__}(name='{self.name}', date='{self.date}')"


def list_portfolios() -> list:
    """List all portfolio_sims decending by date"""
    query = select(models.PortfolioSimulator).order_by(desc(models.PortfolioSimulator.date))
    ps_orm_list = [elem[0] for elem in get_session().execute(query).all()]
    return [Portfolio.load(sim.id) for sim in ps_orm_list]
