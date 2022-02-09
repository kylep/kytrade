# kytrade.api

These are the upstream APIs

## Alphavantage

Alphavantage was the first API I tried. It's really easy to use, but their free data doesn't
include splits or dividends on the daily stock prices so long-term data is not really useful.
They want $50/month for the useful data, which is not bad at scale but expensive while getting
set up. If they have a $10/month offering with the splits and dividends I wouldn't be checking
other APIs out.


## Stock-Shark

Stock-Shark has the ability to actually interact with some brokerages, though it might not support
any that are available in Canada.

Free includes 150 requests a day, all APIs (!) and their broker integration.

Status: I can't get the token to work, getting 400 errors about bad tokens.

## Alpaca API

Their broker API's pricing is not public, "contact sales"... It seems to have comission-free
trades, but their brokerages aren't available in Canada.

Only $9/month for their "Unlimited" account, the Free one is limited to 30 symbols.

Their free API uses IEX for its data, so I don't see the value of going through Alpaca unless I
plan to pay them. I have no problem with paying once I get things working, but so far I'm not
seeing what I want here.


## IEX

From cloud.iexapis.com, IEX has a pretty intuitive API and an interesting credit model. They do
restrict some features from free users. My main gripe with these guys is their data only goes back
15 years, so I wouldn't be able to backtest for example the dot-com crash.


## IBKR TWS API

Like everything else I've seen from IBKR, it's really great in theory and really difficult to work
with in execution. TWS in general is this massive feature-rich ball of mud that looks straight out
of the early 2000's an has refused to update since. For trading I use Questrade's IQ Edge to figure
out what I want to do, then grudgingly use TWS or their often broken web UI to place trades, so
this is no surprise.

- First you have to go to their site to download and launch the TWS or a Gateway service on your
  workstation. From there, you can enable the API on localhost. You can probably enable it on
  0.0.0.0 but I don't see any authentication mechanism to that seems like a terrible idea.
- Next you need to write your API client to be multithreaded since it uses a worker model
- Then you need to extend two base classes with your own custom class to handle the events
  that get triggered when you query for things. It looks like most people just write scripts that
  then print the data to their screen so they can consume it with something more normal
- Once all of that is done, you can comb through their extensive yet still unclear documentation to
  try and get *anything* done.

I think long-term this might be the best tool for the job, especially once I want to do the
"autopilot" feature, but short term I'd sooner pay any company that offers an intuitive REST API
then deal with their bizarre approach to enabling automation.

After all of this I still have no idea how far back the data I can get from them goes, or if it is
adjusted for splits and such. It's just that hard to get working.

I've tried downloading other people's scripts to see how they work, and they don't either.

I tried a 3rd party library and it does seem to work, only to find that their data is not old
enough for my backtesting. I think I'll buy a month of another service, get their old data, then
cancel it and just take good care of my database.


## QuesTrade API

With the exception of ETFs, Questrade's fees are really high compared to IBKR. Having said that,
I might be able to get useful historical data from them.


## EODHistoricalData

[these guys](https://eodhistoricaldata.com/) seem to have some pretty old data, like Ford back to
the 1970's. Originally I'd hoped I could get stuff right through the 1900's but anything before
around the year 2000 is hard to find. I haven't tried them out yet but their prices seem pretty
normal.


## Yahoo Finance

So, I keep reading that they have discontinued their APIs and you can't use Yahoo Finance any more,
yet there are libraries out there and their data seems to go way back. Tempting!
