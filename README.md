# KyTrade

_A daily stock portfolio simulator for backtesting TA strategies_



> While this is open-source, understand that it is experimental.
  *It would be unwise to use this software without speaking to me first.* --  Kyle


---


# Demo

## 1. Buy and Hold QQQ

This demo can be executed interactively, or by running `bin/demos/1_bah_qqq.sh`

This demo shows the PortSim simulating a Buy-and-Hold strategy for QQQ, a NASDAQ 100 Index ETF.

 - The simulation runs from the dates of 2010-01-01 to 2020-01-01.
 - The initial 100 shares of QQQ are added using `--comp` to execute a deposit of their exact
   value to the portfolio when buying them. They are purchased at market close.
 - The date is advanced.
   - Automatic operations (Strategies) can execute each day at the open and close of the market.
     (*not implemented yet*)
   - In this scenario no Strategies are employed. The days pass without touching the portfolio.
 - A summary of the actions taken over that time is printed. In this scenario, not much.
 - A CSV file is generated so you can generate tables in Excel

```
kt init database-tables
kt ps create qqq-bah --date 2010-01-01
kt ps list
kt ps tx buy-stock qqq-bah --ticker QQQ --qty 100 --close --comp
kt ps tx list qqq-bah
kt ps advance qqq-bah --to-date 2020-01-01
kt ps describe qqq-bah
mkdir -p output
kt ps value-history --csv qqq-bah | tee output/qqq-bah-2010-01-01-to-2020-01-01.csv
```



---

# Status

See the [todo list](todo.md)

---


# Installation

This procedure is written on a MacBook but it should work anywhere that Docker can run with only
minor differences (such as with installing the MySQL client packages).


## Python package & CLI

Write an exports.sh file `vi exports.sh`
```
export SQL_PASS=...
export ALPHAVANTAGE_API_KEY=...
export STOCKSHARK_API_KEY=...
```

source the export file (need to do this each time you open your terminal)
```
source export.sh
```


On MacOS, if you don't have the mysql client installed:
```
brew install mysql
```

Make a virtualenv and install the app.
...The archflags var is required on macos else mysql client errors.
```
virtualenv --python=python3 env/
ARCHFLAGS="-arch x86_64" pip install -e .
```


## TWS Python API

IBKR doesn't distrubute the TWS API library on Pypy, so you can't just pip install it from the
internet.

[Download the library](https://interactivebrokers.github.io/) then unzip it and install it.
Then you can import the `ibapi` module.

```
mkdir twsapi
mv twsapi_macunix.976.01.zip twsapi
unzip twsapi_macunix.976.01.zip
cd IBJts/source/pythonclient
pip install .
```


## Database

### Local Database

[*install docker*](https://docs.docker.com/get-docker/)

Start a local database using Docker:
```
bin/start-new-database.sh
```

### Remote Database

Use environment variables to specify the remote database:
```
export SQL_HOST="127.0.0.1"
export SQL_PORT=3306
export SQL_USER="root"
export SQL_PASS="FooBarBaz"
export SQL_DATABASE="trade"
```


---



# Usage

Show that the CLI is installed correctly:
```
kt version
kt
```



## Setup

Initialize the database by creating the tables
```
kt init database-tables
```

Save up to 20 yrs of history for a given ticker to the database - example SPY
```
kt sm download-daily-stock-prices SPY
```

You can populate the stocks list by importing index fund JSON dumps. Some are saved in the git
checkout under `data/index-funds`
```
kt sm load-datahub-stocks data/index-funds/nasdaq100.json
kt sm load-datahub-stocks data/index-funds/sp500.json
```

Load historical data for each stock in the database
```
bin/download-historical-data.sh
```

## Stock Market

The Stock Market stores data outside of portfolios. Currently it stores daily stock prices.
Operated using `kt sm`, which stands for "kytrade stock market", the StockMarket entity also
computes various metadata about each tracked stock.

List all of the stocks that the Stock Market knows about:
```
kt sm list-stocks

# For bash scripting, you can filter to the tickers:
kt sm list-stocks --symbols
```


Download the price history for a given ticker
```
kt sm download-daily-stock-prices [TICKER]
```

List the price history of a given ticker. See the help output for optional filtering arguments.
```
kt sm print-daily-prices --help
```


### Stock Screener

Various TA metadata are computed for each stock and can be printed in a table using the screener.
```
kt sm screener
```


## Portfolio Simulator

### Creating and deleting portfolios

List all current portfolio simulator instances.
The ID and name printed can both be used with the other `kt ps` commands.
```
kt ps list
```

Create a simulated portfolio instance, starting the simulation at a given date.
```
kt ps create [NAME] --date [YYYY-MM-DD]
```

Delete a portfolio simulator instance. The numeric ID can be found from `kt ps list`.
```
kt ps delete [ID]
```


### Manually operating the portfolio

Add some funds to the portfolio simulator.
`[PS ID]` refers to the name or id of the portfolio simulator.
```
kt ps tx deposit [PS ID] --usd [QTY]
```

You can also simulate withdrawing money, for example in a retirement scenario
```
kt ps tx withdraw [PS ID] --usd [QTY]
```

Buy some shares - see `--help` for shorthand options
```
kt ps tx buy-stock [PS ID] --ticker [TICKER] --qty [QUANTITY] [--open/--close] [--comp/--no-comp]
```

Sell some shares
```
kt ps tx sell-stock [PS ID] --ticker [TICKER] --qty [QUANTITY] [--open/--close]
```

List the trasactions of a portfolio including buys, sells, deposits and withdrawls
```
kt ps tx list [PS ID]
```

Simulate advancing time by one day. Each day, trading strategies are applied. Once "at open" then
again "at close" using the associated prices. A new value history entry is created for each day.

```
kt ps advance [PS ID]
```

Advance time to a specific date
```
kt ps advance [PS ID] -d [YYYY-MM-DD]
```

Display detailed statistics about the portfolio
```
kt ps describe [PS ID]
```

Print the value of the portfolio over time
```
kt ps value-history[PS ID]
```

To create charts from the data, currently the easiest approach is to export the value history to
a CSV file then generate one with Excel or another spreadsheet and charting tool.

The `value-history` command has an optional `--csv` argument, which combined with piping the
output to a file can create your csv
```
mkdir output/
kt ps balance-history[PS ID] --csv > output/my_portfolio.csv
```


---


# Dev Tools

Install dev requirements:
```
pip install -r dev-requirements.py
```

Format the code
```
bin/format
```

Lint the code
```
bin/lint
```

Run the unit tests
```
# without coverage stats
bin/unit-test
# with coverage stats
bin/unit-test-coverage
```

## Debugging SQL

You can turn on the SQL echo mode using the following environment variable.
Set it to `False` to disable it.
```
export SQLA_ECHO=True
```
