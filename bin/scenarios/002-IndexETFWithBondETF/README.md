# 002-IndexETFWithBondETF

## To execute

Run `./Scenario002.sh`


## Details

This backtest scenario will simulate a traditional stocks + bonds portfolio, except using ETFs.
At the time of running this, `kytrade` doesn't support actual bonds, so two popular bond ETFs are
chosen. The stock ETF selected is the usual VTI since it's so popular in the FIRE community, though
SPY or QQQ or whatever would also be interesting. Notably *not* being tested is the leveraged
"hedge-fundies excellent adventure" scenario, as it will be tested in its own scenario.

An initial investment of $100,000 will be invested.

The first set of experiments will set up 3 baselines with buy and hold, then compare quarterly
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

This scenario dips its toes into [Modern Portfolio Theory][https://www.investopedia.com/terms/m/modernportfoliotheory.asp]
by comparing a portfolio two holdings. One is non-correlated and the other is somewhat inversely
correlated.

## Symbols

- `VTI`: Vanguard Total Stock Market ETF
  - div yield of ~1.5% not currently implemented
- `BND`: Vanguard Total Bond Market ETF
  - it has super low volatility but very little growth
  - div yield of 2.1% not currently implemented
  - 0.07 correlation with VTI (from https://www.portfoliovisualizer.com/asset-correlations)
- `TLT`: iShares 20+ Year Treasury Bond ETF
  - high liquidity, high volatility
  - div yield of ~1.6% not currently implemented
  - -0.31 correlation with VTI



## Start date

It would be really nice to backdate things further. It might be worth running VTI and TLT back to
2002, but to make the test fair all of the first rounds of the test will start and `BND`'s oldest
data point, `2007-04-10`.

A new feature was implemented in `kt sm describe` so the output is valid JSON, allowing it to be
used with `jq` and `jless` for filtering.

```
kt sm describe VTI | jq .start -r
# 2001-06-15

kt sm describe BND | jq .start -r
# 2007-04-10

kt sm describe TLT | jq .start -r
# 2002-07-30
```

## Open Questions

 - What will the results of the test be?


---


# Results Table

|               Name                |   Start    |    End     |    Positions     |    Cash    |    Value    | CAGR % | MDD % | Sharpe |
|-----------------------------------|------------|------------|------------------|------------|-------------|--------|-------|--------|
|         S002-100.VTI-BAH          | 2007-04-10 | 2022-02-22 |     VTI=1386     |   $48.61   | $300,602.71 |  7.77  | 56.63 | 0.598  |
|      S002-50.VTI-50.CASH-BAH      | 2007-04-10 | 2022-02-22 |     VTI=693      | $50,024.31 | $200,301.35 |  4.84  | 29.38 | 0.722  |
|         S002-100.BND-BAH          | 2007-04-10 | 2022-02-22 |     BND=1329     |   $6.04    | $108,292.96 |  0.54  | 11.18 | 0.191  |
|         S002-100.TLT-BAH          | 2007-04-10 | 2022-02-22 |     TLT=1143     |   $67.51   | $158,475.88 |  3.13  | 28.44 | 0.652  |
|      S002-50.VTI-50.BND-BAH       | 2007-04-10 | 2022-02-22 | BND=664,VTI=693  |   $64.95   | $204,444.71 |  4.99  | 28.98 | 0.719  |
|      S002-50.VTI-50.TLT-BAH       | 2007-04-10 | 2022-02-22 | TLT=571,VTI=693  |  $101.77   | $229,513.71 |  5.79  | 21.29 | 0.683  |
| S002-50.VTI-50.BND-RBAL-Quarterly | 2007-04-10 | 2022-02-22 | BND=1192,VTI=442 |   $26.03   | $192,997.89 |  4.56  | 31.77 | 0.702  |
| S002-50.VTI-50.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-22 | TLT=881,VTI=583  |  $294.00   | $248,815.34 |  6.35  | 25.17 | 0.654  |

Or adjusted for splits/dividends:

|               Name                |   Start    |    End     |    Positions     |    Cash    |    Value    | CAGR % | MDD % | Sharpe |
|-----------------------------------|------------|------------|------------------|------------|-------------|--------|-------|--------|
|         S002-100.VTI-BAH          | 2007-04-10 | 2022-02-22 |     VTI=1840     |   $11.09   | $399,015.09 |  9.84  | 55.45 |  0.54  |
|      S002-50.VTI-50.CASH-BAH      | 2007-04-10 | 2022-02-22 |     VTI=920      | $50,005.54 | $249,507.54 |  6.41  | 28.88 | 0.688  |
|         S002-100.BND-BAH          | 2007-04-10 | 2022-02-22 |     BND=2096     |   $11.37   | $170,793.45 |  3.67  | 9.31  | 0.814  |
|         S002-100.TLT-BAH          | 2007-04-10 | 2022-02-22 |     TLT=1767     |   $47.88   | $244,936.41 |  6.19  | 26.58 | 0.633  |
|      S002-50.VTI-50.BND-BAH       | 2007-04-10 | 2022-02-22 | BND=1048,VTI=920 |   $11.23   | $284,904.27 |  7.35  | 24.94 | 0.658  |
|      S002-50.VTI-50.TLT-BAH       | 2007-04-10 | 2022-02-22 | TLT=883,VTI=920  |   $57.77   | $321,934.74 |  8.23  | 17.42 | 0.605  |
| S002-50.VTI-50.BND-RBAL-Quarterly | 2007-04-10 | 2022-02-22 | BND=1726,VTI=639 |  $102.21   | $279,303.84 |  7.2   | 28.46 | 0.645  |
| S002-50.VTI-50.TLT-RBAL-Quarterly | 2007-04-10 | 2022-02-22 | TLT=1263,VTI=837 |  $150.33   | $356,692.95 |  8.96  | 21.92 | 0.569  |


