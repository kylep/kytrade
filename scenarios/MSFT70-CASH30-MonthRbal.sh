#!/bin/bash
# Invest $100,000 USD into brokerage account at an old point in time
# Every month, rebalance it so you have 30% CASH

START="1994-01-01"
END="2022-02-11"
NAME="MSFT70-CASH30-MonthRbal"
ACTION="REBALANCE-MSFT70-CASH30"
CONDITION="START-OF-MONTH"

# Create a portfolio, add cash, then buy MSFT with 70% of your cash
kt ps create -d START $NAME
kt ps tx deposit $NAME --usd 1000000
kt ps tx buy-stock-by-price $NAME -t MSFT --cost 70000

# Define the rebalance strategy action
kt strat action create rebalance $ACTION --stock MSFT=70 --cash 30

# Define a rebalance condition
kt strat condition create start-of-month $CONDITION

# Link the condition to the action in this portfolio
kt strat create $NAME -- description "Monthly rebalance 70% Microsoft 30% cash"
kt strat add-conditional-action $NAME --condition $CONDITION --action $ACTION
kt ps strat add $NAME $NAME

# advance the portfolio to the end date
kt ps advance $NAME --to-date $END

