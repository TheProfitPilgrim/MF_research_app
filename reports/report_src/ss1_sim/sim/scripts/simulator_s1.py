import pandas as pd
from datetime import date
from filtering_backtest import get_top_funds
from rebalancing_backtest import backtest_with_rebalancing
import time

start_time = time.time()

end_date = date(2025,2,13)
min_days = 400
top_n_alpha = 470

rb_freqencies = ["18 months", "24 months", "36 months"]

start_date_arr = [date(2024,2,10), date(2023,2,10), date(2022,2,10), date(2021,2,10), date(2020,2,10), date(2019,2,10), date(2018,2,10), date(2017,2,10), date(2016,2,10), date(2015,2,10)]

columns_title = ["sim_section", "start_date", "end_date", "min_days", "top_n_alpha", "rebalance", "rebalance_count", "portfolio_returns", "index_returns"]
df_sim_results = pd.DataFrame(columns=columns_title)
length = len(df_sim_results)

for i in start_date_arr:
    start_date = i
    for j in rb_freqencies:
        if j == "No": 
            x, portfolio_return, index_return = get_top_funds(min_days, top_n_alpha, start_date, end_date)
            length = len(df_sim_results)
            df_sim_results.loc[length] = ["2.6", start_date, end_date, min_days, top_n_alpha, j, 0, portfolio_return, index_return]
        else :
            y, portfolio_return, index_return, rebalance_count = backtest_with_rebalancing(start_date, end_date, min_days, top_n_alpha, j)
            length = len(df_sim_results)  # Get current length (next index)
            df_sim_results.loc[length] = ["2.6", start_date, end_date, min_days, top_n_alpha, j, rebalance_count, portfolio_return, index_return]

df_sim_results.to_csv("sim_2.6.csv", index=False)
end_time = time.time()
total_time = end_time - start_time
print(f"Simulation Completed in time {total_time}")