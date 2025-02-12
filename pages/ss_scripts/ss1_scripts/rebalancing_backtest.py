import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from pages.ss_scripts.ss1_scripts.filtering_backtest import get_top_funds

def validate_rebalancing(start_date, end_date, rebalance_freq):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    duration_days = (end_date - start_date).days

    min_duration = {
        "Monthly": 30,
        "Quarterly": 90,
        "Semi-Annual": 180,
        "Annual": 365
    }

    if duration_days < min_duration[rebalance_freq]:
        return False, f"Time period is too short for {rebalance_freq} rebalancing. Choose a longer duration or lower frequency."
    return True, None

def backtest_with_rebalancing(start_date, end_date, min_days, top_n_alpha, rebalance_freq):

    df_mf_raw = pd.read_csv(os.path.join("Data", "Input", "mf_eom.csv"))
    df_index_raw = pd.read_csv(os.path.join("Data", "Input", "nifty_eom.csv"))

    df_mf_raw["nav_date"] = pd.to_datetime(df_mf_raw["nav_date"], dayfirst=True)
    df_index_raw["Date"] = pd.to_datetime(df_index_raw["Date"], dayfirst=True)
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    current_date = start_date
    portfolio_value = 1000  
    rebalancing_dates = []
    between_rebalance_return_arr = []
    all_pfs = pd.DataFrame({"Rebalance Date": pd.to_datetime([]), "Portfolio": pd.Series([], dtype="object")})

    rebalance_map = {
        "Monthly": relativedelta(months=1),
        "Quarterly": relativedelta(months=3),
        "Semi-Annual": relativedelta(months=6),
        "Annual": relativedelta(years=1),
    }

    while current_date <= end_date:
        
        rebalancing_dates.append(current_date)
        next_rebalance_date = current_date + rebalance_map[rebalance_freq]
        pf, between_rebalance_pf_return, x  = get_top_funds(min_days, top_n_alpha, current_date, next_rebalance_date)
        between_rebalance_return_arr.append(between_rebalance_pf_return)
        new_row = pd.DataFrame({"Rebalance Date": [current_date], "Portfolio": [pf]})
        all_pfs = pd.concat([all_pfs, new_row], ignore_index=True) 
        current_date = next_rebalance_date
    
    for i in between_rebalance_return_arr:
        portfolio_value = portfolio_value*(1+i/100)
    
    portfolio_return = ((portfolio_value / 1000) - 1) * 100 

    index_start = df_index_raw[df_index_raw["Date"] >= start_date].sort_values(by="Date").head(1)
    index_end = df_index_raw[df_index_raw["Date"] <= end_date].sort_values(by="Date").tail(1)

    index_return = 0
    if not index_start.empty and not index_end.empty:
        index_start_value = index_start["Close"].values[0]
        index_end_value = index_end["Close"].values[0]
        index_return = ((index_end_value - index_start_value) / index_start_value) * 100

    num_rebalances = len(rebalancing_dates) - 1

    return all_pfs, portfolio_return, index_return, num_rebalances