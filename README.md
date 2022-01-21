# KyTrade

Some python-based trading & investing tools I'm writing for myself. This is open-source because I
open-source basically everything. I've learned a ton from other people's open-source projects.
It would be unwise to use this software without speaking with me first. - Kyle


## Status

- The command-line basically works, though the historical data could be improved.
- Right now this will exclusively simulate purchase/sale executions at open and close.
- This version only tracks stock markets, no forex/bonds/crypto/futures.
- Currently only uses daily data, no inter-day information.
- I'm not paying for the alphavantage subscription so any tickers that have had splits will be
  incorrect.
- Dividends are not yet factored in so everything will seem worse, particularly high-dividend
  positions.
- I'm thinking about writing a simple web UI to display charts and such, have not started it

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

Start a local database usind Docker:
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


Show that it's installed correctly:
```
kt version
kt
```

## Setup

Initialize the database by creating the tables
```
kt init database-tables
```

Save up to 20 yrs of history for a given ticker to the local db - example SPY
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
kt ps add-funds [PS ID] --usd [DOLLARS]
```

Buy some shares - see `--help` for shorthand options:
```
kt ps tx buy-stock [PS ID] --ticker [TICKER] --qty [QUANTITY] [--open/--close] [--comp/--no-comp]
```

Sell some shares:
```
kt ps tx sell-stock [PS ID] --ticker [TICKER] --qty [QUANTITY] [--open/--close]
```

List the trasactions of a portfolio:
```
kt ps tx list [PS ID]
```



## Displaying saved data

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
