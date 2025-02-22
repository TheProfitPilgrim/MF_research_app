# What is the ideal rebalancing frequency? 

In [SS_1 Report](https://github.com/TheProfitPilgrim/MF_Backtest_app/blob/main/reports/Report%20ss_1.md), the Annual or No rebalancing frequencies seemed to give the maximum returns. But this is far from conclusive - there are numerous rebalancing frequencies (like 18 or 24 months) that can be tested out between rebalancing once in 12 months and not rebalancing at all. 

This document considers 3 additional rebalancing frequencies,  18, 24 and 36 months,  apart from the original four - 3, 6 and 12 months and No rebalance and compares them. 

The data points are reduced for it to make logical sense. If the rebalance frequency is set to "Once in 36 months" when the start and end date only span 2 yrs (24 months), then the 36 month will act as a "No rebalancing" case thus not being useful for comparison. Thus for this experiment, the start and end date chosen are greater than 3 years apart. 

The number of funds in the portfolio (top_n_alpha) has been varied and the min track record criteria has been taken to be 400 days. 

Graph 1 : Comparison of arithmetic mean of cumulative portfolio returns for different rebalancing_frequency 
![gr1]()

