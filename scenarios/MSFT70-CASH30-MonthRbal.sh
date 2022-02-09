#!/bin/bash
# Invest $100,000 USD into brokerage account at an old point in time
START="1994-01-01"
NAME="MSFT70-CASH30-MonthRbal"
kt ps create -d START $NAME
kt ps tx deposit $NAME --usd 1000000
kt ps tx buy-stock-by-price $NAME -t MSFT --cost 60000

