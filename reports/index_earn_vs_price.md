## Intro
In [SS 1 _report](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/Report%20ss_1.md)

The broad goal of this study is to look at different indices's price vs earnings relationship across time in different indices in different markets.

Data info
1. Top 100 companies by Mcap are Large cap cos
2. From 101 to 250 is Mid cap
3. Rest are small/micro cap

All indian indices data are from https://www.niftyindices.com/reports/historical-data
S&P 500 data from https://shillerdata.com/

### 1. Correlation between Earnings and Price 

| Index Name         | Rank    | Category  | Date Range| Correlation b/w Price and Earnings |
|--------------------|---------|-----------|-----------|------------------------------------|
| Nifty 50           | 1-50    | Large cap |1999 - 2025| 0.97344                            |
| Nifty Next 50      | 51-100  | Large cap |1999 - 2025| 0.93398                            |
| Nifty Midcap 150   | 101-250 | Mid cap   |2016 - 2025| 0.857727                           |
| Nifty Smallcap 250 | 251-500 | Small cap |2016 - 2025| 0.87173                            | 
| Nifty Microcap 250 | 501-750 | Micro cap |2021 - 2025| 0.95026                            |
| S & P 500          | 1-500   | Large cap |1927 - 2024| 0.97391                            |

These cover the top 750 cos in Indian market (large cap) ( mcap of the smallest co is 4500 cr)

* As expected, the absolute value of correlation (close to 1, where 1 is perfect correlation) of all these indices indicates that there is quite a strong linear relation b/w the earnings level and price of an index, i.e, they both increase / decrease together.

Large Cap Indices : 

* If we consider the S & P 500 data, it is almost a ***century*** of data. The correlation is ~0.974. The Nifty 50 has 25 year data and the correlation is almost the same ~0.973. This goes to show, that in the long run, the earnings and price levels are almost perfectly correlated.
* This kinda makes sense - large cap stocks are generally more widely followed, more liquid so in some sense, more "efficient". 

Other Indices : 




