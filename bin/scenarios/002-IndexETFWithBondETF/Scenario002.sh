#!/bin/bash
set -e

# download the data
for symbol in VTI BND TLT; do kt sm download-daily-stock-prices $symbol; done

# Set the comission to 0
export TX_BROKERAGE_COMISSION=0

# define the strategy condition and actions
kt strat condition create start-of-day "DAILY"
kt strat condition create start-of-month "MONTHLY"
kt strat condition create start-of-quarter "QUARTERLY"
kt strat condition create start-of-year "YEARLY"

kt strat action create rebalance "RBAL-50.VTI-50.BND" --stock "VTI=50" --stock "BND=50"
kt strat action create rebalance "RBAL-50.VTI-50.TLT" --stock "VTI=50" --stock "TLT=50"
kt strat action create rebalance "RBAL-40.VTI-60.TLT" --stock "VTI=40" --stock "TLT=60"
kt strat action create rebalance "RBAL-60.VTI-40.TLT" --stock "VTI=60" --stock "TLT=40"
kt strat action create rebalance "RBAL-75.VTI-25.TLT" --stock "VTI=75" --stock "TLT=25"
kt strat action create rebalance "RBAL-90.VTI-10.TLT" --stock "VTI=90" --stock "TLT=10"

kt strat create "Quarterly-RBAL-50.VTI-50.BND"
kt strat create "Quarterly-RBAL-50.VTI-50.TLT"
kt strat create "Quarterly-RBAL-40.VTI-60.TLT"
kt strat create "Quarterly-RBAL-60.VTI-40.TLT"
kt strat create "Quarterly-RBAL-75.VTI-25.TLT"
kt strat create "Quarterly-RBAL-90.VTI-10.TLT"
kt strat create "Daily-RBAL-50.VTI-50.TLT"
kt strat create "Monthly-RBAL-50.VTI-50.TLT"
kt strat create "Yearly-RBAL-50.VTI-50.TLT"

kt strat add-conditional-action "Quarterly-RBAL-50.VTI-50.BND" --condition "QUARTERLY" --action "RBAL-50.VTI-50.BND"
kt strat add-conditional-action "Quarterly-RBAL-50.VTI-50.TLT" --condition "QUARTERLY" --action "RBAL-50.VTI-50.TLT"
kt strat add-conditional-action "Quarterly-RBAL-40.VTI-60.TLT" --condition "QUARTERLY" --action "RBAL-40.VTI-60.TLT"
kt strat add-conditional-action "Quarterly-RBAL-60.VTI-40.TLT" --condition "QUARTERLY" --action "RBAL-60.VTI-40.TLT"
kt strat add-conditional-action "Quarterly-RBAL-75.VTI-25.TLT" --condition "QUARTERLY" --action "RBAL-75.VTI-25.TLT"
kt strat add-conditional-action "Quarterly-RBAL-90.VTI-10.TLT" --condition "QUARTERLY" --action "RBAL-90.VTI-10.TLT"
kt strat add-conditional-action "Daily-RBAL-50.VTI-50.TLT" --condition "DAILY" --action "RBAL-50.VTI-50.TLT"
kt strat add-conditional-action "Monthly-RBAL-50.VTI-50.TLT" --condition "MONTHLY" --action "RBAL-50.VTI-50.TLT"
kt strat add-conditional-action "Yearly-RBAL-50.VTI-50.TLT" --condition "YEARLY" --action "RBAL-50.VTI-50.TLT"



# shared portfolio args
START=2007-04-10
END=2022-02-24
START_CASH=100000
HALF_START_CASH=50000


# simulations

PORTFOLIO="S002-100.VTI-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-50.VTI-50.CASH-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-100.BND-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s BND --cost $START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-100.TLT-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost $START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-50.VTI-50.BND-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s BND --cost $HALF_START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-50.VTI-50.TLT-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost $HALF_START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-50.VTI-50.BND-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s BND --cost $HALF_START_CASH
kt ps strat add $PORTFOLIO "Quarterly-RBAL-50.VTI-50.BND"
kt ps advance $PORTFOLIO --to-date $END


PORTFOLIO="S002-50.VTI-50.TLT-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost $HALF_START_CASH
kt ps strat add $PORTFOLIO "Quarterly-RBAL-50.VTI-50.TLT"
kt ps advance $PORTFOLIO --to-date $END


PORTFOLIO="S002-40.VTI-60.TLT-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost 40000
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost 60000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-40.VTI-60.TLT"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-60.VTI-40.TLT-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost 60000
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost 40000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-60.VTI-40.TLT"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-75.VTI-25.TLT-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost 75000
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost 25000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-75.VTI-25.TLT"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-90.VTI-10.TLT-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost 90000
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost 10000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-90.VTI-10.TLT"
kt ps advance $PORTFOLIO --to-date $END


PORTFOLIO="S002-50.VTI-50.TLT-RBAL-Daily"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost $HALF_START_CASH
kt ps strat add $PORTFOLIO "Daily-RBAL-50.VTI-50.TLT"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S002-50.VTI-50.TLT-RBAL-Monthly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost $HALF_START_CASH
kt ps strat add $PORTFOLIO "Monthly-RBAL-50.VTI-50.TLT"
kt ps advance $PORTFOLIO --to-date $END


PORTFOLIO="S002-50.VTI-50.TLT-RBAL-Yearly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s VTI --cost $HALF_START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TLT --cost $HALF_START_CASH
kt ps strat add $PORTFOLIO "Yearly-RBAL-50.VTI-50.TLT"
kt ps advance $PORTFOLIO --to-date $END
