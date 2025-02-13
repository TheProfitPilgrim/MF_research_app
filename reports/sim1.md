# Report : SS_1

Date : 13/02/2025 

[Link to try out](https://mfproject.streamlit.app/ss_1) 

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

## 1.1 : 

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


