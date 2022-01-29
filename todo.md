# TODO List

## Soon

- impl `ps.max_drawdown`, `ps.max_drawdown_percent` -> float
- impl `sm.max_drawdown`, `sm.max_drawdown_percent` -> float
- impl `ps.longest_drawdown_duration` -> datetime.delta
- impl `sm.longest_drawdown_duration` -> datetime.delta
- impl `ps.sharpe_ratio` -> float
- impl `sm.sharpe_ratio` -> float
- impl treynor ratio (not to be confused with google's treynor curve)
  - portfolio beta
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

## Wish List

- Web UI
- Interday data in backtests and interday strategy triggers
- Options
- Bonds
- S&P Futures
- Commodities
- Crypto
- Self-Driving Portfolio (online hands-free algo-trader)

# Done!

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

