# Report : SS_1

Date : 13/02/2025 

[Link to try out](https://mfproject.streamlit.app/ss_1) 

Data : 

Tldr; 🥱😴 : 
1. For rebalancing frequency, either No rebalancing or Annual rebalancing give the best portfolio returns
2. Number of funds in the portfolio doesn't really seem to affect the portfolio returns that much
3. For track record,   

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

## Section 1

Effect of Note 1 in this section : I've considered 400 days which is ~1 year. So for the average calculations, I'm considering up to the recent 9 year performances instead of 10. 

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

![gr1](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/report_media/Picture1.png)

Graph 2 : The different portfolio returns for each time period

![gr2](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/report_media/Picture2.png)

* The X-axis in the above graph is the time period between start and end date in years
* It is clear that the Quarterly and Semi-Annual reblancing perform worse than the Annual and No rebalancing cases. However, between the Annual and No rebalancing cases, there isn't a clear winner as of now. But this is for a single case of top_n_alpha.

Lets see the effect of different rebalancing frequencies' behaviour if the top_n_alpha (no. of funds in portfolio) is changed. The top_n_alpha values used for this plot are 5, 10, 20, 50, 100

Graph 3 : Box and Whisker plot to study effect of rebalance_frequency

![gr3](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/report_media/Picture3.png)

1. Observation: Based on the above graph, the "No Rebalance" strategy appears to have the highest median portfolio return (the "X" is highest in this box), followed closely by "Annual". "Semi-Annual" is next, and "Quarterly" has the lowest median.
Interpretation: On average, "No Rebalance" and "Annual" tend to generate the highest portfolio returns compared to the other rebalancing frequencies, according to this plot. "Quarterly" rebalancing tends to generate the lowest returns on average.

2. Observation: "Quarterly" has the smallest box. The boxes for "Semi-Annual" and "Annual" are larger than "Quarterly," and the box for "No Rebalance" is the largest.
Interpretation: "Quarterly" rebalancing demonstrates the most consistent returns (least variability) within the middle 50% of the data. "No Rebalance" exhibits the least consistent returns.

3. Observation: "Quarterly" has the shortest whiskers. The whiskers for "Semi-Annual" are longer than "Quarterly's." "Annual" is longer than "Semi-Annual", and "No Rebalance" has by far the longest upper whisker.
Interpretation: "Quarterly" rebalancing results in the smallest overall range of returns (most consistent). "No Rebalance" can achieve higher maximums because it has the longest upper whisker but it also has much lower returns.

4. Observation: "Quarterly" has a couple of outliers on the high end (above the upper whisker). "No Rebalance" has one very high outlier.
Interpretation: "Quarterly" rebalancing occasionally leads to exceptionally high returns. "No Rebalance" shows that there was at least one year in the simulation where it drastically overperformed.


## 1.2 : Studying number of funds in portfolio 

* Exact same simulation as 1.1 but with 1 change, the number of funds in the portfolio (top_n_alpha) is varied. The top_n_alpha used are 5,10,20(same as 1.1), 50, 100, 200 and ALL the funds. 

Graph 4 : Pivot chart to study effect of top_n_alpha

![gr4](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/report_media/Picture4.png)

For number of funds in an equiweighted portfolio, for :
   * No rebalancing case : Clear trend of - lesser the number of funds in the portfolio, better the returns
   * Annual : A weaker trend of lesser the no of funds, better the returns
   * Quarterly and Semi-Annual : No of funds in the portfolio doesn't seem to matter that much

Overall, the number of funds forming the portfolio doesn't seem to affect the portfolio return much for an equiweighted case
