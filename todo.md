# TODO List

## Soon

- AlphaVantage free data not useful (no split/div data), $50/month is expensive. Before buying Pro:
  - POC of Stock-Shark API https://stock-shark.com/developers
    - Also works for autopilot
  - POC of Alpaca API https://alpaca.markets/data
    - Also works for autopilot
  - Investigate Yahoo Finance python lib
  - Polygon seems way overpriced
  - Investigate IBKR - though it looks like people use TWS exports mostly and I don't want to
  - https://iexcloud.io/docs/api/
    - Alpaca appears to use this for their free tier, might be better off going to the src
- move the metadata for the screener into a table so it be pre-computed
- move the computation of metadata into calc so portsim can use it  too
- impl `ps.sharpe_ratio` -> float
- impl `sm.sharpe_ratio` -> float
- impl treynor ratio (not to be confused with google's treynor curve)
  - portfolio beta
- impl sortino ratio
- `ps.profit` should really be `ps.return_on_investment`
- impl `ps.discounted_cash_flows`
- Impl a simple on-open strategy of some sort to prove the concept
  - Idea: "Paper Hands" strategy
    - Start with $10,000
    - Buy [TICKER], max affordable
    - Every green yesterday close, sell a share on open (1% if more than 100 shares)
    - Every red yesterday, buy as many shares as you can afford
- Imp a rebalance at n-interval strategy suchs as HFEA
- Impl commissions
- Handle dividends
- Handle splits
- Extend the "Base" base class to a "Day" base class so I'm not duck-typing it

## Wish List

- Web UI
- Interday data in backtests and interday strategy triggers
- Options
- Bonds
- S&P Futures
- Commodities
- Crypto
- Self-Driving Portfolio (online hands-free algo-trader)


## Maybe
- Refactor to replace "ticker" with "symbol", pretty sure thats the more correct term


# Done!


- rename `kt sm describe-stock` to `kt sm describe` since the `s` in `sm` is already "stock"
- replaced `kt sm list-daily` command with `kt sm screener` since its more like a stock screener
- impl max drawdowns and associated dates
- bollinger bands calculation and screener
- standard deviations and variances in screener
- impl `simple_moving_average` in sm - used the new metadata dict
- impl `kt sm list-daily`
- Added CAGR to portfolio and describe output
- `kt ps describe` shows table of useful derived stats
- getting started demo
- simulation DB operations much optimized
  - lazy and eager loading where appropriate
- Command-line functional
- advance to next day
- bulk advance day
- live sim progress tracker (for fun)

