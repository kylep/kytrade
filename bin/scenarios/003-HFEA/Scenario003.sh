#!/bin/bash
set -e

# download the data
for symbol in UPRO TQQQ TMF; do
  kt sm download-daily-stock-prices $symbol
  sleep 1  # Yahoo does not appreciate too many requests too fast
done

# Set the comission to 0
export TX_BROKERAGE_COMISSION=0
export ADJUST_FOR_DIVIDENDS=TRUE

# define the strategy condition and actions
kt strat condition create start-of-day "DAILY"
kt strat condition create start-of-month "MONTHLY"
kt strat condition create start-of-quarter "QUARTERLY"
kt strat condition create start-of-year "YEARLY"

kt strat action create rebalance "RBAL-40.UPRO-60.TMF" --stock "UPRO=40" --stock "TMF=60"
kt strat action create rebalance "RBAL-55.UPRO-45.TMF" --stock "UPRO=55" --stock "TMF=45"
kt strat action create rebalance "RBAL-60.UPRO-40.TMF" --stock "UPRO=60" --stock "TMF=40"
kt strat action create rebalance "RBAL-60.TQQQ-40.TMF" --stock "TQQQ=60" --stock "TMF=40"
kt strat action create rebalance "RBAL-30.TQQQ-30.UPRO--40.TMF" --stock "UPRO=30" --stock "TQQQ=30" --stock "TMF=40"

kt strat create "Quarterly-RBAL-40.UPRO-60.TMF"
kt strat create "Quarterly-RBAL-55.UPRO-45.TMF"
kt strat create "Quarterly-RBAL-60.UPRO-40.TMF"
kt strat create "Quarterly-RBAL-60.TQQQ-40.TMF"
kt strat create "Quarterly-RBAL-30.UPRO-30.TQQQ-40.TMF"

kt strat add-conditional-action "Quarterly-RBAL-40.UPRO-60.TMF" --condition "QUARTERLY" --action "RBAL-40.UPRO-60.TMF"
kt strat add-conditional-action "Quarterly-RBAL-55.UPRO-45.TMF" --condition "QUARTERLY" --action "RBAL-55.UPRO-45.TMF"
kt strat add-conditional-action "Quarterly-RBAL-60.UPRO-40.TMF" --condition "QUARTERLY" --action "RBAL-60.UPRO-40.TMF"
kt strat add-conditional-action "Quarterly-RBAL-60.TQQQ-40.TMF" --condition "QUARTERLY" --action "RBAL-60.TQQQ-40.TMF"
kt strat add-conditional-action "Quarterly-RBAL-30.UPRO-30.TQQQ-40.TMF" --condition "QUARTERLY" --action "RBAL-30.UPRO-30-TQQQ-40.TMF"



# shared portfolio args
START=$(kt sm describe TQQQ | jq .start -r)
END=$(kt sm describe TQQQ | jq .end -r)
START_CASH=100000


# simulations

PORTFOLIO="S003-100.UPRO-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s UPRO --cost $START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S003-100.TQQQ-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TQQQ --cost $START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S003-100.TMF-BAH"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TMF --cost $START_CASH
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S003-40.UPRO-60.TMF-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s UPRO --cost 60000
kt ps tx buy-stock-by-price $PORTFOLIO -s TMF --cost 40000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-40.UPRO-60.TMF"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S003-55.UPRO-45.TMF-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s UPRO --cost 60000
kt ps tx buy-stock-by-price $PORTFOLIO -s TMF --cost 40000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-55.UPRO-45.TMF"
kt ps advance $PORTFOLIO --to-date $END


PORTFOLIO="S003-60.UPRO-40.TMF-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s UPRO --cost 60000
kt ps tx buy-stock-by-price $PORTFOLIO -s TMF --cost 40000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-60.UPRO-40.TMF"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S003-60.TQQQ-40.TMF-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s TQQQ --cost 60000
kt ps tx buy-stock-by-price $PORTFOLIO -s TMF --cost 40000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-60.UPRO-40.TMF"
kt ps advance $PORTFOLIO --to-date $END

PORTFOLIO="S003-30.TQQQ--30.UPRO-40.TMF-RBAL-Quarterly"
echo $PORTFOLIO
kt ps create -d $START $PORTFOLIO
kt ps tx deposit $PORTFOLIO  --usd $START_CASH
kt ps tx buy-stock-by-price $PORTFOLIO -s UPRO --cost 30000
kt ps tx buy-stock-by-price $PORTFOLIO -s TQQQ --cost 30000
kt ps tx buy-stock-by-price $PORTFOLIO -s TMF --cost 40000
kt ps strat add $PORTFOLIO "Quarterly-RBAL-30.UPRO-30.TQQQ-40.TMF"
kt ps advance $PORTFOLIO --to-date $END


