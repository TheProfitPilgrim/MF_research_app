# Report : SS_1

Date : 13/02/2025 

[Link to try out](https://mfproject.streamlit.app/ss_1) 

[Data](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/report_data/sim_1.csv) 

Tldr 🥱😴 : 
1. For rebalancing frequency, either No rebalancing or Annual rebalancing give the best portfolio returns
2. Number of funds in the portfolio doesn't really seem to affect the portfolio returns that much but general trend is, more concentrated = better returns. 
3. As the track record requirement of the fund decreases, the portfolio returns increase
4. If someone had used ss_1 to form a portfolio anytime in the past decade, they are guaranteed to outperform the Nifty 50 and Nifty 500 (and that too by almost 2x in most cases).
5. However portfolios formed using ss_1 underperform Nifty Midcap 100 in all time frames. The reason for this is suspected to be the Midcap Index's massive "fragile" rise in Price without the Earnings to back it up - This is investigated in [Indices : Price vs Earnings](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/index_earn_vs_price.md)

### Goals and assumptions : 
* Test a selection system based on 2 parameters :
  1. The fund's all time (from the earliest available [data](https://github.com/TheProfitPilgrim/MF_Backtest_app/tree/main/Data/Input) for each fund) cumulative outperformance vs the Nifty 50.
  2. How long the fund has been active for - track record
  
* Form an equiweighted portfolio with and without rebalancing and study the effects of various parameters like size of portfolio, track record of the funds and rebalancing effects on the formed portfolio's performance

### Drawbacks and Limitations of SS_1
1. Uses cummulative returns : 
$$\frac{\text{Final} - \text{Initial}}{\text{Initial}} \times 100 \space$$
which is not ideal for an absolute evaluation. Future systems will use a better return metric. However, some insights can be drawn using it uniformly as a comparitive tool
2. Ideal case scenario : Does not factor in any 'real-life' factors like exit-load or other overheads

An initial experiment to roughly see if there is any scope of outperformance by forming a portfolio of funds. Aim to get the "ballpark" figures and a general direction to head in forming portfolios. 

* Inputs for SS_1 are :
  
  1. start_date - the initial date for forming portfolios and for return calculations 
  2. end_date - the final date for forming portfolios and for return calculations
  3. top_n_alpha - the number of individual funds in the portfolio - the selection of top N funds based on the fund's annualised all time excess return over the Nifty 50 
  4. min_days - the minimum "time since inception" that each of the funds in the portfolio must have
  5. rebalance_frequency - Quarterly, Semi-Annual, Annual or "No" (for no rebalance)

Note 1 : Setting the min_days too high is going to restrict the data that we can work with.
Suppose we set min_days as 1000 that ~3 yrs and start date somewhere in 2015, SS_1 is going to result in an empty portfolio since even the oldest funds in the data have only 1 year of track record. 
     
* In each section, some of the inputs from above will be kept constant and some others will be allowed to change to see the effect that they have on the overall portfolio performance  

## Section 1 : Studying the variables in ss_1

Effect of Note 1 in this section : If've considered 400 days which is ~1 year, for the average calculations, I'm considering up to the recent 9 year performances instead of 10 (10-years is the span of total raw data available in the csv). 

## 1.1 : Studying rebalance frequencies

### Fixed Variables
1. End date = 13/02/25
2. No. of funds in portfolio = 20
3. Min time since inception for funds (days) = 400 

### Changing Variables
1. Start Dates : 13/02/2024, 13/02/2023, 13/02/2022 ... and so on until 13/02/2015

* For given fixed variables, change the start date to get time periods ranging from recent 1yr to recent 10yrs
* Find out the No rebalance, Qtr, Semi-Ann and Ann rebalance portfolio returns for each of these periods
* Compare the frequencies and their effect on return

Graph 1 : Grouping each rebalancing frequency and finding the average of portfolio returns across different time periods 

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture1.png)

Graph 2 : The different portfolio returns for each time period

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture2.png)

* The X-axis in the above graph is the time period between start and end date in years
* It is clear that the Quarterly and Semi-Annual reblancing perform worse than the Annual and No rebalancing cases. However, between the Annual and No rebalancing cases, there isn't a clear winner as of now.

Graph 3 : Box and Whisker plot to study effect of rebalance_frequency

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture3.png)

1. Observation : The "Annual" and "No Rebalance" appear to have the highest median portfolio return (the "X" is highest in these boxes). "Semi-Annual" is next, and "Quarterly" has the lowest median.
Interpretation: On average, "Annual" and "No Rebalance" tend to generate the highest portfolio returns compared to the other rebalancing frequencies. "Quarterly" rebalancing tends to generate the lowest returns on average.

2. Observation: "Quarterly" has the smallest box and the smallest range of returns. The boxes for "Semi-Annual" and "Annual" are larger than "Quarterly," and the box for "No Rebalance" is larger than the rest.
Interpretation: "Quarterly" rebalancing demonstrates the most consistent returns (least variability) within the middle 50% of the data. "No Rebalance" exhibits the least consistent returns.

4. Observation: "Quarterly" has two outlier on the high end (above the upper whisker). "No Rebalance" has two outlier on the high end.
Interpretation: "Quarterly" and "No Rebalance" rebalancing occasionally leads to exceptionally high returns compared to the rest.

The Annual or No rebalancing frequencies seemed to give the maximum returns. But this is far from conclusive - there are numerous rebalancing frequencies (like 18 or 24 months) that can be tested out between rebalancing once in 12 months and not rebalancing at all. 

Consider 3 additional rebalancing frequencies,  18, 24 and 36 months,  apart from the original four - 3, 6 and 12 months and No rebalance and compare them. 

The data points are reduced for it to make logical sense. If the rebalance frequency is set to "Once in 36 months" when the start and end date only span 2 yrs (24 months), then the 36 month will act as a "No rebalancing" case thus not being useful for comparison. Thus for this experiment, the start and end date chosen are greater than 3 years apart. 

The number of funds in the portfolio (top_n_alpha) has been varied and the min track record criteria has been taken to be 400 days. 

Graph 4 : Comparison of arithmetic mean of cumulative portfolio returns for different rebalancing_frequency 

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture6.png)

## 1.2 : Studying number of funds in portfolio 

The above was for a single value of top_n_alpha (20). Lets see the effect of different rebalancing frequencies' behaviour if the top_n_alpha (no. of funds in portfolio) is changed. The top_n_alpha values used for this plot are 5, 10, 20, 50, 100

* Exact same simulation as 1.1 but with 1 change, the number of funds in the portfolio (top_n_alpha) is varied. The top_n_alpha used are 5,10,20(same as 1.1), 50, 100, 200 and ALL the funds. 

Graph 5 : Pivot chart to study effect of top_n_alpha

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture4.png)

For number of funds in an equiweighted portfolio, for :
   * No rebalancing case : Clear trend of - lesser the number of funds in the portfolio, better the returns
   * Annual : A weaker trend of lesser the no of funds, better the returns
   * Quarterly and Semi-Annual : No of funds in the portfolio doesn't seem to matter that much

Overall, the number of funds forming the portfolio doesn't seem to affect the portfolio return much for an equiweighted case

## 1.3 : Studying min_days in portfolio 

As discussed in note 1, the data points decrease as we keep increaing the min_days : 
| min_days | No. of data points (out of 40) |
|----------|--------------------------------|
| 100      | 40                             |
| 400      | 36                             |
| 700      | 36                             |
| 1000     | 32                             |
| 1300     | 28                             |
| 1600     | 24                             |
| 2000     | 20                             |

But since average returns is being used, it is still useful for comparison.

Graph 6 : Pivot chart to study effect of min_days

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture5.png)

As expected, the returns of the portfolio increase as we reduce the need for a track record. Take for example funds with ~100 days track record. It means that the fund was formed 3 months ago. And in the bull market peak, with Nifty touching 26k levels, it is only expected that these funds have insanely good "All-time" alpha. 

Sometime in the future, we'd have to strike an ideal balance in this aspect to prevent selecting funds with a highly biased sample data period. 

## Section 2 : Effect of date of portfolio creation on the portfolio return 

## 2.1 : Probability of formed portfolio beating Nifty 50 

One Year Period

* Sorted by all time cumulative alpha
* No of funds in each portfolio (top_n_alpha)   = 20 
* Track record (min_days)                       = 1000 days
* Start date                                    = 01/01/2024
* End date                                      = 01/01/2025
* New portfolio is formed                       = every month
* No. of portfolios                             = 12 - 1 = 11 (We cannot get the results of the most recently formed portfolio)
* No rebalancing - portfolio is formed and held till end date

Date is matched with each portfolio for calculating the Index return

Graph 7 : Bar Chart to compare Portfolio vs Index Returns for the 11 portfolios formed

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture7.png)

From the graph, 11 is most recently formed portfolio (formed 1 month ago) and 1 is the portfolio formed 1 year ago. 

Three Year Period

Graph 8 : Bar Chart to compare Portfolio vs Index Returns for the 35 portfolios formed

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture8.png)

Five Year Period

Graph 9 : Bar Chart to compare Portfolio vs Index Returns for the 59 portfolios formed

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture9.png)

### 10 Year Period

Graph 10 : Bar Chart to compare Portfolio vs Index Returns for all the portfolios formed

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture10.png)

Probability of outperformance = 100%
Thus we can see that if someone had used ss_1 to form a portfolio anytime in the past decade, they are guaranteed to outperform the Nifty 50. 

## 2.2 : Probability of formed portfolio beating Nifty 50 & Nifty 500

The same plots of sections 2.1 - 2.4 is compared with similar plots of that done using Nifty 500 : 

Graph 11 : Bar chart with all 4 for 1 year period

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture11.png)

Graph 12 : Line chart with all 4 for 3 year period

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture12.png)

Graph 13 : Bar chart with all 4 for 5 year period

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture13.png)

Graph 14 : Bar chart with all 4 for 10 year period

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture14.png)

Probability of outperformance = 100%
Thus we can see that if someone had used ss_1 to form a portfolio anytime in the past decade, they are guaranteed to outperform Nifty 500.

## 2.3 : Probability of formed portfolio beating Nifty Midcap 100

| Time Period  | Outperformance Probability |
|-------------|--------------------------|
| One Year    | 9% (1 / 11)              |
| Three Years | 8.6% (3 / 35)            |
| Five Years  | 6.7% (4 / 59)            |
| Ten Years   | 41.37% (48 / 116)        |

Graph 15, 16, 17, 18 : Above table's data points visualised

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture15.png)

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture16.png)

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture17.png)

![gr](https://raw.githubusercontent.com/TheProfitPilgrim/MF_Backtest_app/main/reports/report_media/Picture18.png)

We can see that someone would have been way better off investing in Nifty Midcap 100 in the past decade compared to the system's portfolio. 

Many of the portfolios formed contained a lot of Midcap and small cap equity funds. If mid and small cap stocks had risen up by a lot more than Nifty 50 and 500, it makes sense that the Index, Mid / small cap funds are going to do so much better than the Nifty 50. 

But was this price outperformance backed by sufficient earnings increase? Is it sustainable? 
Explored in : [Indices : Price vs Earnings](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/index_earn_vs_price.md)
