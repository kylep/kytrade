# TODO List

## Soon

- impl `ps.max_drawdown` and print it in describe table
- `ps.profit` should really be `ps.return_on_investment`
- impl `ps.discounted_cash_flows`
- Calculate SMA's
- Impl a simple on-open strategy of some sort to prove the concept
  - Idea: "Paper Hands" strategy
    - Start with $10,000
    - Buy [TICKER], max affordable
    - Every green yesterday close, sell a share on open (1% if more than 100 shares)
    - Every red yesterday, buy as many shares as you can afford
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

- Added CAGR to portfolio and describe output
- `kt ps describe` shows table of useful derived stats
- getting started demo
- simulation DB operations much optimized
  - lazy and eager loading where appropriate
- Command-line functional
- advance to next day
- bulk advance day
- live sim progress tracker (for fun)

