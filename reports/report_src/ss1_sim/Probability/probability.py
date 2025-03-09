import pandas as pd
from datetime import date
from filtering_backtest import get_top_funds
import numpy as np

begin_date = date(2015, 1, 1)
end_date = date(2025, 1, 1)

dates = []
all_portfolios = []
portfolio_returns = []
index_returns = []

current_date = begin_date
while current_date <= end_date:
    dates.append(current_date)
    if current_date.month == 12:
        current_date = date(current_date.year + 1, 1, 1)
    else:
        current_date = date(current_date.year, current_date.month + 1, 1)
j = 0
min_days = 400
top_n_alpha = 20

for i in dates:
    start_date = i
    portfolio, portfolio_ret, index_ret = get_top_funds(min_days, top_n_alpha, start_date, end_date, "Nifty Midcap 100")
    all_portfolios.append(portfolio)
    portfolio_returns.append(portfolio_ret)
    index_returns.append(index_ret)
    j+=1
    print(f"{j}` done ...")

combined_portfolios = pd.DataFrame()

# Iterate through the list of portfolios
for i, portfolio in enumerate(all_portfolios):
    # Add the current portfolio to the combined DataFrame
    combined_portfolios = pd.concat([combined_portfolios, portfolio], ignore_index=True)
    
    # Add a blank row after each portfolio (except the last one)
    if i < len(all_portfolios) - 1:
        blank_row = pd.DataFrame([[np.nan] * len(portfolio.columns)], columns=portfolio.columns)
        combined_portfolios = pd.concat([combined_portfolios, blank_row], ignore_index=True)

combined_portfolios.to_csv('all_portfolios10y_nfmcap100.csv', index=False)


df_pf_ret = pd.DataFrame(portfolio_returns)
df_in_ret = pd.DataFrame(index_returns)

df_pf_ret.to_csv('all_pf_returns10y_nfmcap100.csv', index=False)
df_in_ret.to_csv('all_index_returns10y_nfmcap100.csv', index=False)
