# Index ETF Rebalanced w/ Cash

This backtest scenario intends to determine if there is an advantage to keeping some % of your
portfolio in cash instead of dumping the whole thing into an index fund. The FIRE community
typically endorses down-cost-averaging into VTI throughout your career. This backtest attempts
some modifications of that plan by rebalancing at various intervals and %s to hopefully "buy low
and sell high" along the way.

One problem with using VTI is I only have data back to `2001-06-15`. I'd really like to have
captured the dot-com crash as I think this strategy will do well during it. Yahoo gives  SPY data
from `1993-01-29` so maybe some extra tests at the end depending on conclusions using SPY are
warranted.

The comissions are set to $0 since I suspect the rebalancing will not perform great in the first
place.


## Conclusions

- On monthly rebalance, the higher % cash you use, the lower CAGR. Buy-and-hold has highest CAGR.
- Higher cash % does lower the max drawdown, if only slightly more than it lowers the CAGR
- Rebalancing more often is worse. It raises the MDD and lowers the CAGR. Did not expect that one.
- UPRO has the same behaviour in general.


### Results Table

Without dividends:

|          Name          |   Start    |    End     | Positions  |    Cash     |     Value     | CAGR % | MDD % |
|------------------------|------------|------------|------------|-------------|---------------|--------|-------|
|      S001-VTI-BAH      | 2001-06-15 | 2022-02-22 |  VTI=1796  |   $25.66    |  $394,014.18  |  6.85  | 56.64 |
|  S001-VTI-50-Monthly   | 2001-06-15 | 2022-02-22 |  VTI=480   | $109,267.38 |  $214,564.98  |  3.76  | 33.1  |
|  S001-VTI-75-Monthly   | 2001-06-15 | 2022-02-22 |  VTI=1002  | $76,244.40  |  $296,053.14  |  5.39  | 45.92 |
|  S001-VTI-95-Monthly   | 2001-06-15 | 2022-02-22 |  VTI=1587  | $18,936.97  |  $367,077.16  |  6.49  | 54.74 |
|   S001-VTI-75-Daily    | 2001-06-15 | 2022-02-22 |  VTI=691   | $50,412.32  |  $201,996.99  |  3.46  | 47.61 |
| S001-VTI-75-Quarterly  | 2001-06-15 | 2022-02-22 |  VTI=981   | $75,065.34  |  $290,267.32  |  5.29  | 45.24 |
|   S001-VTI-75-Yearly   | 2001-06-15 | 2022-02-22 |  VTI=988   | $79,210.99  |  $295,948.54  |  5.38  | 44.94 |
|     S001-UPRO-BAH      | 2009-06-25 | 2022-02-22 | UPRO=82940 |    $0.85    | $4,743,339.45 | 35.64  | 76.82 |
| S001-UPRO-75-Quarterly | 2009-06-25 | 2022-02-22 | UPRO=22557 | $488,964.05 | $1,778,998.88 | 25.53  | 62.37 |

With dividends:

|          Name          |   Start    |    End     | Positions  |    Cash     |     Value     | CAGR % | MDD % | Sharpe |
|------------------------|------------|------------|------------|-------------|---------------|--------|-------|--------|
|      S001-VTI-BAH      | 2001-06-15 | 2022-02-22 |  VTI=2620  |   $32.07    |  $568,179.07  |  8.82  | 55.44 | 0.477  |
|  S001-VTI-50-Monthly   | 2001-06-15 | 2022-02-22 |  VTI=578   | $132,478.78 |  $257,818.08  |  4.71  | 32.15 | 0.695  |
|  S001-VTI-75-Monthly   | 2001-06-15 | 2022-02-22 |  VTI=1329  | $101,363.10 |  $389,556.75  |  6.84  | 44.79 | 0.578  |
|  S001-VTI-95-Monthly   | 2001-06-15 | 2022-02-22 |  VTI=2308  | $27,834.70  |  $528,324.50  |  8.43  | 53.46 | 0.496  |
|   S001-VTI-75-Daily    | 2001-06-15 | 2022-02-22 |  VTI=1368  | $99,125.27  |  $395,776.07  |  6.92  | 44.45 | 0.574  |
| S001-VTI-75-Quarterly  | 2001-06-15 | 2022-02-22 |  VTI=1312  | $100,341.22 |  $384,848.42  |  6.77  | 44.1  | 0.576  |
|   S001-VTI-75-Yearly   | 2001-06-15 | 2022-02-22 |  VTI=1321  | $106,327.02 |  $392,785.87  |  6.88  | 43.89 | 0.574  |
|     S001-UPRO-BAH      | 2009-06-25 | 2022-02-22 | UPRO=85197 |    $0.87    | $4,717,358.76 | 35.93  | 76.82 | 0.119  |
| S001-UPRO-75-Quarterly | 2009-06-25 | 2022-02-22 | UPRO=29070 | $630,276.68 | $2,239,882.58 | 28.07  | 62.37 | 0.205  |



### Open Questions

- Data didn't include the dot-com crash. I think with huge crashes the cash positions might perform
  better. Still, betting on a dot-com style crash for your portfolio allocation to pay off doesn't
  seem like a good plan.


---


## S001-VTI-BAH

This is the standard lump-sum buy-and-hold approach.

- Buy $100,000 worth of VTI on 2001-06-15
- Do nothing. Run the simulation to 2022-02-22

## S001-VTI-50-Monthly

This uses 50% VTI, 50% cash. Rebalanced monthly on the 1st day of the month.

- Buy $100,000 worth of VTI on 2001-06-15
- The `START-OF-MONTH` condition doesn't exist yet, so instantiate it
- Define a rebalance action for 50% VTI and 50% Cash: `RBAL-VTI-50`
- Create a strategy to bind the condition to the action `Monthly-RBAL-VTI-50`
- Create the portfolio and give it $100,000
- Buy all the VTI
- Bind the strategy to the portfolio
- Advance the simulation to 2022-02-22

## S001-VTI-75-Monthly

Same as S001-VTI-50-Monthly except 75% VTI instead of 50%.


## S001-VTI-95-Monthly

Same as S001-VTI-50-Monthly except 95% VTI instead of 50%.


## S001-UPRO-BAH

UPRO is much more volatile than VTI, it's a 3x leveraged index fund tracking SPY. I wonder if it
would benefit from rebalancing instead?

I have data starting from `2009-06-25`.


## S001-UPRO-75-Quarterly

Checking to see if rebalancing a more volatile stock is better. The CAGR is still insanely high,
but the MDD is also still very high.
