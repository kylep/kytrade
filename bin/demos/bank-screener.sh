#!/bin/bash

bin/reset-database.sh

for symbol in RY.TO TD.TO BNS.TO BMO.TO CM.TO; do
  kt sm download-daily-stock-prices symbol
done

kt sm screener
