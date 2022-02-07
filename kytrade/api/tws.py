"""IBKR TWS API"""
import threading
import time

# ibapi comes from https://interactivebrokers.github.io/
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.common import BarData


# TODO: Move these to constants file if I keep them
PAPER_TRADE = True
PROD_PORT = 7496
PAPER_PORT = 7497
HOST = "127.0.0.1"
CLIENT_ID = 123
MKT_DATA_TYPES = {"live": 1, "frozen": 2, "delayed": 3, "delayed_frozen": 4}
CONN_STATES = {"CS_DISCONNECTED": 0, "CS_CONNECTING": 1, "CS_CONNECTED": 2, "CS_REDIRECT": 3}


# See https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/
class IBapi(EWrapper, EClient):
    """International Brokers API"""

    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. Id {reqId} tickType: {TickTypeEnum.to_str(tickType)} Price: {price}")

    def tickSize(self, reqId, tickType, size):
        print(f"Tick Size. Id: {reqId} tickType {TickTypeEnum.to_str(tickType)} Size: {size}")

    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)


class IbkrNotConnectedError(Exception):
    """The session is not connected"""


def get_stock_contract(symbol: str, exchange: str = None) -> Contract:
    """Return a Contract() object for a stock query"""
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = exchange if exchange else "NYSE"
    contract.currency = "USD"
    return contract
    # TODO: What is this for?
    # client.app.reqContractDetails()


class IbkrClient:
    """Client handling async application session state"""

    _instance = None

    def __init__(self):
        """Call instance() instead"""
        raise RuntimeError("Call IbkrClient.instance() instead")

    @classmethod
    def instance(cls):
        """IbkrClient singleton instatiator"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            self = cls._instance
            self.keep_alive = True
            self.app = IBapi()
            self.thread = threading.Thread(target=self.__thread, daemon=True)
            self.thread.start()
            for attempt in range(0, 4):
                if self.app.connState == CONN_STATES["CS_CONNECTED"]:
                    print(self.app)
                    print("CONNECTED")
                    break
                time.sleep(1)  # Sleep interval to allow time for connection to server (ugh...)
            if self.app.connState != CONN_STATES["CS_CONNECTED"]:
                raise NotConnectedError(f"IBKR TWS ConnState: {self.app.connState}")
            cls._instance = self  # TODO: Verify if I need this - call-by-reference... right?
        assert cls._instance.thread.is_alive(), "Thread must be alive!"
        return cls._instance

    def __thread(self):
        """Run the TWS session in a dedicated thread"""
        print("LAUNCHING THREAD")
        self.app.connect(HOST, PAPER_PORT, CLIENT_ID)
        self.app.run()
        while self.keep_alive:
            time.sleep(0.1)

    def __del__(self):
        """destructor disconnects session"""
        self.keep_alive = False  # Causes __thread to end
        time.sleep(0.15)  # thread takes 0.1s to close
        self.app.disconnect()

    def stock_streaming_mkt_price(self, symbol: str):
        """Use the IBKR Contract object to get the current price of a stock
           I'm really not sure what's up with this, its entirely unclear how to use it
        """
        contract = get_stock_contract(symbol)
        ticker_id = 1  # unique value, returned market data is identified by ticker_id
        generic_tick_list = ""  # "commma delimited list of generic tick types"
        snapshot = False  # if True "cancel market data subscription" after returning
        regulatory_snapshot = False  # cost $0.01 USD each, leave False
        market_data_options = []  # "For internal use only" by TWS
        # market data types: https://interactivebrokers.github.io/tws-api/market_data_type.html
        # Frozen market data is the last data recorded at market close.
        self.app.reqMarketDataType(MKT_DATA_TYPES["delayed_frozen"])
        return self.app.reqMktData(
            reqId=ticker_id,
            contract=contract,
            genericTickList=generic_tick_list,
            snapshot=snapshot,
            regulatorySnapshot=regulatory_snapshot,
            mktDataOptions=market_data_options,
        )

    def stock_historical_data(self, symbol: str):
        """Get the historical data"""
        # https://interactivebrokers.github.io/tws-api/historical_bars.html
        contract = get_stock_contract(symbol)
        # reqHistoricalData(
        #  reqId: int, contract: ibapi.contract.Contract, endDateTime: str, durationStr: str,
        #  barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool,
        #  chartOptions: list)
        # RTH is "regular trrade hours"
        ticker_id = 1
        return self.app.reqHistoricalData(
            reqId=ticker_id,
            contract=contract,
            endDateTime="",
            durationStr="1 Y",
            barSizeSetting="1 day",
            whatToShow="MIDPOINT",
            useRTH=0,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )
