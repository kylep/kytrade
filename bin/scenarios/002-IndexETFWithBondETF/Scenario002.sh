#!/bin/bash
set -e

# download the data
for symbol in VTI BND TLT; do kt sm download-daily-stock-prices $symbol; done

# Set the comission to 0
export TX_BROKERAGE_COMISSION=0

# define the strategy condition and actions
kt strat condition create start-of-quarter "QUARTERLY"

kt strat action create rebalance "RBAL-50.VTI-50.BND" --stock "VTI=50" --stock "BND=50"
kt strat action create rebalance "RBAL-50.VTI-50.TLT" --stock "VTI=50" --stock "TLT=50"

kt strat create "Quarterly-RBAL-50.VTI-50.BND"
kt strat create "Quarterly-RBAL-50.VTI-50.TLT"

kt strat add-conditional-action "Quarterly-RBAL-50.VTI-50.BND" --condition "QUARTERLY" --action "RBAL-50.VTI-50.BND"
kt strat add-conditional-action "Quarterly-RBAL-50.VTI-50.TLT" --condition "QUARTERLY" --action "RBAL-50.VTI-50.TLT"


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
