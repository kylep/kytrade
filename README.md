# KyTrade

Some python-based trading & investing tools

# Installation

This procedure is written on a MacBook but it should work anywhere that Docker can run with only
minor differences (such as with installing the MySQL client packages).


[*install docker*](https://docs.docker.com/get-docker/)


Write an exports.sh file `vi exports.sh`
```
export SQL_PASS=...
export ALPHAVANTAGE_API_KEY=...
```

source the export file (need to do this each time you open your terminal)
```
source export.sh
```


Start a database:
```
bin/start-new-database.sh
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

List all current portfolio simulator instances
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


## Displaying saved data

Show historical values
```
kt print daily-prices --help
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
