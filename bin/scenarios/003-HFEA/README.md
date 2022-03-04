# 003-HFEA

[HEDGEFUNDIE's Excellent Adventure](https://www.optimizedportfolio.com/hedgefundie-adventure/)

- `UPRO`: 3x leveraged S&P 500 Index
- `TQQQ`: 3x leveraged Nasdaq 100 Index
- `TMF`: 3x leveraged 20 year bond ETF

In [the last](../002-IndexETFWithBondETF/README.md) experiment, it was shown that VTI and TLT
worked well together to lower MDD without seriously impacting CAGR. By using leveraged ETFs, a much
higher CAGR can be achieved, at the cost of a much higher MDD and also a small chance of being
wiped out (if, for instance, somehow an index dropped 33% in a day without a circuit breaker
preventing it from doing that.

## Portfolio Simulations:

The first set establishes the baseline numbers.
The standard HFEA strategy uses 60% `UPRO` and 40% `TMF`. Many people use TQQQ instead or mix and
match.

- S003-100.UPRO-BAH
- S003-100.TQQQ-BAH
- S003-100.TMF-BAH
- S003-60.UPRO-40.TMF-RBAL-Quarterly
- S003-60.TQQQ-40.TMF-RBAL-Quarterly
- S003-30.TQQQ--30.UPRO-40.TMF-RBAL-Quarterly


