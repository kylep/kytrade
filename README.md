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
kt download daily-stock-prices QQQ
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

- The command-line is functional
- Advancing detween days works and the value history is logged using daily stock data
- Live profit % tracker slightly slows down simulations but makes them FUN
  - Disable tracker with `--no-print-status` for marginal speed improvement
- daily open/close Stategies are not implemented
- Dividends and splits aren't included in the alphavantage free data. Stock performance will appear
  worse until I pay them...
- Web UI / chart generation not started
- Simulation speed is much improved, simulating ~20yrs takes ~50s. Could still be faster.
  - Database actions are all bulked out and lazy-loaded, they're not the bottleneck now
  - Maybe this can be multi-threaded, multiple portfolio sims can definitely be ran at once
  - Longterm a worker model might be appropriate for high-complexity
  - Rewriting in a faster language is more work than it's worth right now


---


# Installation

This procedure is written on a MacBook but it should work anywhere that Docker can run with only
minor differences (such as with installing the MySQL client packages).


## Python package & CLI

Write an exports.sh file `vi exports.sh`
```
export SQL_PASS=...
export ALPHAVANTAGE_API_KEY=...
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
kt download daily-stock-prices SPY
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



## Displaying market data

Show historical values. Ensure you've downloaded that ticker first.
This is only really useful if you pipe it to a file or want to see limited data.
```
# Show all the saved entries for AAPL
kt print daily-prices --ticker AAPL

# Show the most recent MSFT entry
kt print daily-prices --ticker MSFT --limit 1

# Show the 5 most recent entries of SPY, ending at 2000-01-01
kt print daily-prices --ticker SPY --limit 5 --from-date 2000-01-01
```


## Point-in-time calculations

Calculate Simple Moving Average (SMA) of a stock from a given date, over a range, using the open,
close, high, or low daily value.

```
kt calc sma --help
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
