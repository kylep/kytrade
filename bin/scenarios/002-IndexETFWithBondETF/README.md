# 002-IndexETFWithBondETF


## Conclusions

- Inversely corrolated stocks help reduce MDD disproportionately to their reduction in CAGR.
  - This is probably why you see them used with leverage
- Rebalance intervals do not have consistent impacts on a portfolio. Yearly outperforms quarterly,
  even though in general rebalancing more often increases CAGR and MDD
- `BND` is better to hold for its own sake than `TLT`, but `TLT` balances out an equities portfolio
  better.


## To execute

Run [Scenario002](./Scenario002.sh): `./Scenario002.sh`


## Details

This backtest scenario can simulate a traditional stocks + bonds portfolio, except using ETFs.
At the time of running this, `kytrade` doesn't support actual bonds, so two popular bond ETFs are
chosen. The stock ETF selected is the usual VTI since it's so popular in the FIRE community, though
SPY or QQQ or whatever would also be interesting. Notably *not* being tested is the leveraged
"hedge-fundies excellent adventure" scenario, as it will be tested in its own scenario.

This scenario dips its toes into [Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
by comparing a portfolio w/ two holdings. One is non-correlated and the other is somewhat inversely
correlated.

An initial investment of $100,000 is invested.

The first set of experiments set up 3 baselines with buy and hold, then compare quarterly
rebalancing against them.

 - S002-100.VTI-BAH: 100% VTI Buy and Hold
 - S002-50.VTI-50.CASH-BAH: 50/50 VTI + CASH - From scenario 001
 - S002-100.BND-BAH: 100% BND Buy and Hold
 - S002-100.TLT-BAH: 100% TLT Buy and Hold
 - S002-50.VTI-50.BND-BAH: 50/50 VTI + BND Buy and Hold
 - S002-50.VTI-50.TLT-BAH: 50/50 VTI + TLT Buy and Hold
 - S002-50.VTI-50.BND-RBAL-Quarterly: 50/50 VTI + BND Rebalanced quarterly
 - S002-50.VTI-50.TLT-RBAL-Quarterly: 50/50 VTI + TLT Rebalanced quarterly

`BND` seems to behave sort of like cash without a dividend. With the dividend its total CAGR over
time does seem to be above the current risk-free rate, but very probably lower than the average
risk-free rate over the same duration (which I don't have).

Unsuprisingly VTI + TLT did the best, with dividend adjusted CAGR of `8.96%` and a max drawdown
of only `21.92%`. The Sharpe ratio column is new and I'm not sure that it's right.

The next scenario expands on the `S002-50.VTI-50.TLT-RBAL-Quarterly` scenario by testing `40/60`,
`60/40`,`75/25`, and `90/10` splits of `VTI/TLT`.

- S002-40.VTI-60.TLT-RBAL-Quarterly
- S002-60.VTI-40.TLT-RBAL-Quarterly
- S002-75.VTI-25.TLT-RBAL-Quarterly
- S002-90.VTI-10.TLT-RBAL-Quarterly

Those experiments show sort of a non-linear slider where CAGR goes down along with MDD as the ratio
of TLT increases. There's no objectively best option but the 60/40 (~30% drawdown) seems good for
growth and 50/50 (~22% drawdown) seems good overall.

Next experiments check to see the impact of different rebalance frequencies on the above 50/50
distribution.

 - S002-50.VTI-50.TLT-RBAL-Daily
 - S002-50.VTI-50.TLT-RBAL-Monthly
 - S002-50.VTI-50.TLT-RBAL-Yearly

This experiment shows the MDD get lower as you rebalance less frequently. You'd expect the CAGR to
also go down alongside the MDD, which it mostly does, with one interesting outlier. The yearly
rebalancing actually has a higher CAGR `9.12` than quarterly's `8.81`, making it objectively
better.


---


# Results Table

The data has been sorted to be easier to read.

Adjusted for splits and dividends:

|               Name                |   Start    |    End     |     Positions     |    Value    | CAGR % | MDD % | Sharpe |
|-----------------------------------|------------|------------|-------------------|-------------|--------|-------|--------|
|         S002-100.VTI-BAH          | 2007-04-10 | 2022-02-24 |     VTI=1840      | $398,536.69 |  9.62  | 55.45 | 0.527  |
|      S002-50.VTI-50.CASH-BAH      | 2007-04-10 | 2022-02-24 |      VTI=920      | $249,268.34 |  6.24  | 28.88 | 0.668  |
|         S002-100.BND-BAH          | 2007-04-10 | 2022-02-24 |     BND=2096      | $170,311.37 |  3.63  | 9.31  | 0.805  |
|         S002-100.TLT-BAH          | 2007-04-10 | 2022-02-24 |     TLT=1767      | $241,720.47 |  6.11  | 26.58 | 0.625  |
|      S002-50.VTI-50.BND-BAH       | 2007-04-10 | 2022-02-24 | BND=1048,VTI=920  | $284,424.03 |  7.19  | 24.94 | 0.642  |
|      S002-50.VTI-50.TLT-BAH       | 2007-04-10 | 2022-02-24 |  TLT=883,VTI=920  | $320,088.48 |  8.06  | 17.42 | 0.592  |
| S002-50.VTI-50.BND-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | BND=1726,VTI=639  | $278,740.68 |  7.07  | 28.46 | 0.632  |
| S002-50.VTI-50.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=1263,VTI=837  | $354,176.54 |  8.81  | 21.92 | 0.559  |

Allocation adjustments:

|               Name                |   Start    |    End     |     Positions     |    Value    | CAGR % | MDD % | Sharpe |
|-----------------------------------|------------|------------|-------------------|-------------|--------|-------|--------|
| S002-90.VTI-10.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=279,VTI=1663  | $398,527.62 |  9.63  | 49.42 | 0.529  |
| S002-75.VTI-25.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=686,VTI=1364  | $389,565.13 |  9.48  | 39.64 | 0.536  |
| S002-60.VTI-40.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=1053,VTI=1047 | $370,889.64 |  9.14  | 29.01 | 0.548  |
| S002-50.VTI-50.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=1263,VTI=837  | $354,176.54 |  8.81  | 21.92 | 0.559  |
| S002-40.VTI-60.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=1439,VTI=635  | $334,673.56 |  8.41  | 18.15 | 0.571  |


Frequency adjustments:

|               Name                |   Start    |    End     |     Positions     |    Value    | CAGR % | MDD % | Sharpe |
|-----------------------------------|------------|------------|-------------------|-------------|--------|-------|--------|
|   S002-50.VTI-50.TLT-RBAL-Daily   | 2007-04-10 | 2022-02-22 | TLT=1333,VTI=852  | $369,584.26 |  9.22  | 23.15 | 0.561  |
|  S002-50.VTI-50.TLT-RBAL-Monthly  | 2007-04-10 | 2022-02-22 | TLT=1296,VTI=803  | $353,974.00 |  8.9   | 24.18 | 0.568  |
| S002-50.VTI-50.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-24 | TLT=1263,VTI=837  | $354,176.54 |  8.81  | 21.92 | 0.559  |
|  S002-50.VTI-50.TLT-RBAL-Yearly   | 2007-04-10 | 2022-02-22 | TLT=1342,VTI=823  | $364,568.88 |  9.12  | 20.54 | 0.564  |
|      S002-50.VTI-50.TLT-BAH       | 2007-04-10 | 2022-02-24 |  TLT=883,VTI=920  | $320,088.48 |  8.06  | 17.42 | 0.592  |




---


# Notes


## Symbols

- `VTI`: Vanguard Total Stock Market ETF
  - div yield of ~1.5%, good growth
- `BND`: Vanguard Total Bond Market ETF
  - it has super low volatility but very little growth
  - div yield of 2.1%
  - 0.07 correlation with VTI (from https://www.portfoliovisualizer.com/asset-correlations)
- `TLT`: iShares 20+ Year Treasury Bond ETF
  - high liquidity, high volatility
  - div yield of ~1.6%, some growth
  - -0.31 correlation with VTI

## Start date

It would be really nice to backdate things further. It might be worth running VTI and TLT back to
2002, but to make the test fair all of the first rounds of the test will start and `BND`'s oldest
data point, `2007-04-10`.

A new feature was implemented in `kt sm describe` so the output is valid JSON, allowing it to be
used with `jq` and `jless` for filtering.

```
kt sm describe VTI | jq .start -r  # 2001-06-15
kt sm describe BND | jq .start -r  # 2007-04-10
kt sm describe TLT | jq .start -r  # 2002-07-30
```

Another new feature is allowing to adjust for dividends. You can enable/disable the adjustments now
but running:

```
export ADJUST_FOR_DIVIDENDS=TRUE
export ADJUST_FOR_DIVIDENDS=FALSE
```
