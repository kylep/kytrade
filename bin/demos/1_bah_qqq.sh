#!/bin/bash
set -e
if [[ ! -d bin/ ]]; then echo "ERROR: Run from checkout base"; exit 1; fi
kt init database-tables
kt download daily-stock-prices QQQ
kt ps create qqq-bah --date 2010-01-01
kt ps list
kt ps tx buy-stock qqq-bah --ticker QQQ --qty 100 --close --comp
kt ps tx list qqq-bah
kt ps advance qqq-bah --to-date 2020-01-01
mkdir -p output
kt ps value-history --csv qqq-bah | tee output/qqq-bah-2010-01-01-to-2020-01-01.csv
