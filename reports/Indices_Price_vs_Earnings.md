## Intro
In [SS 1 _report](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/Report%20ss_1.md), the suspected reason for the formed Pfs outperforming Nifty 50, 500 but underperforming Nifty Midcap 100 was the Midcap index's price rally. 

Drawbacks / Issues with this analysis : 
1. Though it looks roughly linearly related, correlation might not be a great way to measure.

The broad goal of this study is to look at different indices's price vs earnings relationship across time in different indices in different markets, using a simple metric for this - correlation. 

Correlation makes sense only if its *linearly* related. Let's check how the relations looks in a scatter plot

| ![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture20.png) | ![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture21.png) |
|-----------------------|-----------------------|
| Nifty 50 | Nifty Next 50 |

| ![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture22.png) | ![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture23.png) |
|-----------------------|-----------------------|
| Nifty Midcap 150 | Nifty Smallcap 250 |

Though not perfect, I think its linear enough to use correlation to analyse. 

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

These cover the top 750 cos in Indian market (large cap) ( mcap of the smallest co is 4500 cr) and S&P 500. 

* As expected, the absolute value of long term correlation (close to 1, where 1 is perfect correlation) of all these indices indicates that there is quite a strong positive relation b/w the earnings level and price of an index, i.e, they both increase / decrease together.

Large Cap Indices : 

* If we consider the S&P 500 data, it is almost a ***century*** of data. The correlation is ~0.974. The Nifty 50 has 25 year data and the correlation is almost the same ~0.973. This goes to show, that in the long run, the earnings and price levels are almost perfectly correlated.
* Nifty Next 50's correlation being lower at 0.933 shows a relatively lower positive relationship

* However, in the short term, they don't always rise and fall together. There is quite some variation. We can see how correlation changes in the short term (1 year rolling window) for Nifty 50 and S&P 500 by plotting the rolling correlation graph.

![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture24.png)

![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture25.png)

We can use the dates to attribute reasons for divergance b/w price and earnings : https://en.wikipedia.org/wiki/Stock_market_crashes_in_India#

* Note : A bottom in the rolling correlation graph does not convey any info on the actual movement of the Price vs Earnings - just that one is moving in opposite direction to the another - it could be :

1. Price decrease when earnings has not really fallen / maybe even increased 
2. Price increase when earnings has not really increased / maybe even fallen

If both had risen or fallen together, the correlation would be positive.

To see how the actual movement has occured, we can take a look at the following graph (% YOY change for the date span) of Nifty 50 : 

![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture26.png)

Now lets compare the different indices' price correlation vs their earnings **in the same period**

* If micro cap index is included, then the date range is going to be constrained to <5 yrs. So lets compare the correlations of Nifty 50, Next 50, Midcap 150 and Smallcap 250 over 2016-2025 period.

![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture19.png) 

Comparitively, the much lower correlation in Nifty Midcap 150 and Small cap 250 is indicative of the divergence in price and earnings changes.

The 4 cases that are interesting are : 

# Market Scenarios: Index vs. Earnings Behavior

| Scenario | Description | When Does It Happen? | Example Cases | Opportunity |
|----------|------------|----------------------|--------------|----------------|
| **1. Both Earnings and Prices Rise** | A strong earnings-driven bull market where fundamentals justify price increases. | Economic expansions, post-recession recoveries, new tech booms | **India (2003-07)** -  corporate earnings surged. **US (2010-19 Bull Market)** - Consistent earnings growth post 2008/9 crisis. | Long-term Long |
| **2. Prices Rise, but Earnings Don’t** | Speculative rally where sentiment drives prices higher without earnings support. | Bubbles | **Dot-com bubble (1999-2000)** - Tech stocks soared without earnings. **Post Covid (2020-21)** - Prices surged post-COVID (in anticipation), but earnings lagged. | Short-term short |
| **3. Prices Drop, but Earnings Stay Strong** | Market panic or fear-driven selling despite stable fundamentals. | Crashes | **COVID Crash (March 2020)** - Sharp market drop, but earnings were stable (at least then, ofc the price reacts in anticipation). **Financial Crisis (2008)** - Many stocks fell due to forced selling. | Short-term long |
| **4. Both Earnings and Prices Decline** | Bear market or recession, where economic downturns lead to lower corporate profits and falling stock prices. | Recessions, crisis periods, sector-specific declines. | **2008-09 Global Financial Crisis** - Banking sector collapse. **Indian econ Slowdown (2011-13)** - High inflation, weak corporate profits. | Long-term short |

* Just because something falls into one of these categories does not mean its an opportunity directly - Let's take Covid for example :

![Graph](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture27.png) 
  
  * The market as soon as it came to know of the lockdown, anticipated that many industries like Aviation / Tourism are not going to be functional and thus fell predicting a fall in corporate earnings (blue).
  * The fall in earnings did eventually happen - so the market wasn't entirely foolish.
  * If someone considered the Covid bottom as a buying opportunity, it can be attributed to these reasons : 
    * Covid will not continue on for say 3 or 5 years and that things will come back to normal ==> Rebound in earnings and price (Long-term long)
    * The market overreacted to the expected fall in earnings ==> Earnings turn out to be better than anticipated even with covid ==> Market corrects for this excess decline (short-term long)

  * After all the vaccinations and lockdown removal, the market again bounced back to pre-covid levels before the earnings actually caught up and even overshot too much on the upper side     
