#!/bin/bash

# Set the comission to 0
export TX_BROKERAGE_COMISSION=0
export ADJUST_FOR_DIVIDENDS=TRUE


START=2001-06-15
END=2022-02-22
START_CASH=100000
SYMBOL=VTI


# S001-VTI-BAH: Buy and Hold
echo "S001-VTI-BAH"

kt ps create -d $START "S001-VTI-BAH"
kt ps tx deposit "S001-VTI-BAH" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-BAH" -s VTI --cost $START_CASH
kt ps advance "S001-VTI-BAH" --to-date $END


# S001-VTI-50-Monthly
echo "S001-VTI-50-Monthly"

kt strat condition create start-of-month "START-OF-MONTH"
kt strat action create rebalance "RBAL-VTI-50" --stock VTI=50 --cash 50
kt strat create "Monthly-RBAL-VTI-50"
kt strat add-conditional-action "Monthly-RBAL-VTI-50"  --condition "START-OF-MONTH" --action "RBAL-VTI-50"

kt ps create -d $START "S001-VTI-50-Monthly"
kt ps tx deposit "S001-VTI-50-Monthly" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-50-Monthly" -s VTI --cost $START_CASH
kt ps strat add "S001-VTI-50-Monthly" "Monthly-RBAL-VTI-50"
kt ps advance "S001-VTI-50-Monthly" --to-date $END


# S001-VTI-75-Monthly
echo "S001-VTI-75-Monthly"

kt strat action create rebalance "RBAL-VTI-75" --stock VTI=75 --cash 25
kt strat create "Monthly-RBAL-VTI-75"
kt strat add-conditional-action "Monthly-RBAL-VTI-75"  --condition "START-OF-MONTH" --action "RBAL-VTI-75"

kt ps create -d $START "S001-VTI-75-Monthly"
kt ps tx deposit "S001-VTI-75-Monthly" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-75-Monthly" -s VTI --cost $START_CASH
kt ps strat add "S001-VTI-75-Monthly" "Monthly-RBAL-VTI-75"
kt ps advance "S001-VTI-75-Monthly" --to-date $END


# S001-VTI-95-Monthly
echo "S001-VTI-95-Monthly"

kt strat action create rebalance "RBAL-VTI-95" --stock VTI=95 --cash 5
kt strat create "Monthly-RBAL-VTI-95"
kt strat add-conditional-action "Monthly-RBAL-VTI-95"  --condition "START-OF-MONTH" --action "RBAL-VTI-95"

kt ps create -d $START "S001-VTI-95-Monthly"
kt ps tx deposit "S001-VTI-95-Monthly" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-95-Monthly" -s VTI --cost $START_CASH
kt ps strat add "S001-VTI-95-Monthly" "Monthly-RBAL-VTI-95"
kt ps advance "S001-VTI-95-Monthly" --to-date $END


#############
# That's the end of changing up the allocations. How about varrying the rate of rebalancing?


# S001-VTI-75-Daily
echo "S001-VTI-75-Daily"

kt strat condition create start-of-day "START-OF-DAY"
kt strat create "Daily-RBAL-VTI-75"
kt strat add-conditional-action "Daily-RBAL-VTI-75"  --condition "START-OF-DAY" --action "RBAL-VTI-75"

kt ps create -d $START "S001-VTI-75-Daily"
kt ps tx deposit "S001-VTI-75-Daily" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-75-Daily" -s VTI --cost $START_CASH
kt ps strat add "S001-VTI-75-Daily" "Daily-RBAL-VTI-75"
kt ps advance "S001-VTI-75-Daily" --to-date $END


# S001-VTI-75-Quarterly
echo "S001-VTI-75-Quarterly"

kt strat condition create start-of-quarter "START-OF-QUARTER"
kt strat create "Quarterly-RBAL-VTI-75"
kt strat add-conditional-action "Quarterly-RBAL-VTI-75"  --condition "START-OF-QUARTER" --action "RBAL-VTI-75"

kt ps create -d $START "S001-VTI-75-Quarterly"
kt ps tx deposit "S001-VTI-75-Quarterly" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-75-Quarterly" -s VTI --cost $START_CASH
kt ps strat add "S001-VTI-75-Quarterly" "Quarterly-RBAL-VTI-75"
kt ps advance "S001-VTI-75-Quarterly" --to-date $END


# S001-VTI-75-Yearly
echo "S001-VTI-75-Yearly"
kt strat condition create start-of-year "START-OF-YEAR"
kt strat create "Yearly-RBAL-VTI-75"
kt strat add-conditional-action "Yearly-RBAL-VTI-75"  --condition "START-OF-YEAR" --action "RBAL-VTI-75"

kt ps create -d $START "S001-VTI-75-Yearly"
kt ps tx deposit "S001-VTI-75-Yearly" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-VTI-75-Yearly" -s VTI --cost $START_CASH
kt ps strat add "S001-VTI-75-Yearly" "Yearly-RBAL-VTI-75"
kt ps advance "S001-VTI-75-Yearly" --to-date $END


# What about UPRO?
START="2009-06-25"

# S001-UPRO-BAH
echo "S001-UPRO-BAH"

kt ps create -d $START "S001-UPRO-BAH"
kt ps tx deposit "S001-UPRO-BAH" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-UPRO-BAH" -s UPRO --cost $START_CASH
kt ps advance "S001-UPRO-BAH" --to-date $END


# S001-UPRO-75-Quarterly
kt strat create "Quarterly-RBAL-UPRO-75"
kt strat action create rebalance "RBAL-UPRO-75" --stock "UPRO=75" --cash 25
kt strat add-conditional-action "Quarterly-RBAL-UPRO-75"  --condition "START-OF-QUARTER" --action "RBAL-UPRO-75"

kt ps create -d $START "S001-UPRO-75-Quarterly"
kt ps tx deposit "S001-UPRO-75-Quarterly" --usd $START_CASH
kt ps tx buy-stock-by-price "S001-UPRO-75-Quarterly" -s UPRO --cost $START_CASH
kt ps strat add "S001-UPRO-75-Quarterly" "Quarterly-RBAL-UPRO-75"
kt ps advance "S001-UPRO-75-Quarterly" --to-date $END



