# kytrade.api

These are the upstream APIs

## Alphavantage

Alphavantage was the first API I tried. It's really easy to use, but their free data doesn't
include splits or dividends on the daily stock prices so long-term data is not really useful.
They want $50/month for the useful data, which is not bad at scale but expensive while getting
set up.


## Stock-Shark

Stock-Shark has the ability to actually interact with some brokerages, though it might not support
any that are available in Canada.

Free includes 150 requests a day, all APIs (!) and their broker integration.

Status: I can't get the token to work, getting 400 errors about bad tokens. Will try later.

## Alpaca API

Their broker API's pricing is not public, "contact sales"... It seems to have comission-free
trades, but it also might not support canadian brokerages.

Only $9/month for their "Unlimited" account, the Free one is limited to 30 symbols.


