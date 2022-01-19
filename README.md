# KyTrade

Some python-based trading & investing tools.

*Status*:
Right now I'm trying to find some alpha, or at least beta,
using exclusively actions at open and close.


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

List all current portfolio simulator instances.
The ID and name printed can both be used with the other `kt ps` commands.
```
kt ps list
```

Create a simulated portfolio instance, starting the simulation at a given date.
```
kt ps create [NAME] --date [YYYY-MM-DD]
```

Add some funds to the portfolio simulator.
`[PS ID]` refers to the name or id of the portfolio simulator.
```
kt ps add-funds [PS ID] --usd [DOLLARS]
```

Buy some shares - see `--help` for shorthand options:
```
kt ps buy-stock [PS ID] --ticker [TICKER] --qty [QUANTITY] [--open/--close] [--comp/--no-comp]
```

Sell some shares:
```
kt ps sell-stock [PS ID] --ticker [TICKER] --qty [QUANTITY] [--open/--close]
```

Delete a portfolio simulator instance. The numeric ID can be found from `kt ps list`.
```
kt ps delete [ID]
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
