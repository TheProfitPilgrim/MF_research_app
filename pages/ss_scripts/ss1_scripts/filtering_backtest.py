import pandas as pd
import os

def get_top_funds(min_days, top_n_alpha, start_date, end_date):
    # Load backtest mutual fund data
    df = pd.read_csv(os.path.join("data", "output", "MF_calc_backtest.csv"))
    
    # Convert start_date and end_date to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter funds based on minimum days
    df_filtered = df[df["Duration (Days)"] >= min_days]

    # Sort by Excess Return (%) and select top N funds
    df_sorted = df_filtered.sort_values(by="Excess Return (%)", ascending=False)
    df_top_backtest = df_sorted.head(top_n_alpha)

    # Load mutual fund NAV data
    df_nav = pd.read_csv(os.path.join("data", "input", "mf_eom.csv"))
    df_nav["nav_date"] = pd.to_datetime(df_nav["nav_date"])

    fund_returns = []
    
    for fund in df_top_backtest['Fund Name']:
        fund_data = df_nav[df_nav['scheme_name'] == fund]

        # Get NAV at or after start_date
        nav_start = fund_data[fund_data["nav_date"] >= start_date].sort_values(by="nav_date").head(1)
        # Get NAV at or before end_date
        nav_end = fund_data[fund_data["nav_date"] <= end_date].sort_values(by="nav_date", ascending=False).head(1)

        if not nav_start.empty and not nav_end.empty:
            nav_start_value = nav_start["nav"].values[0]
            nav_end_value = nav_end["nav"].values[0]
            fund_return = ((nav_end_value - nav_start_value) / nav_start_value) * 100
            fund_returns.append(fund_return)

    # Calculate portfolio return as arithmetic mean
    portfolio_return = sum(fund_returns) / len(fund_returns) if fund_returns else 0

    # Load index data and compute index return
    df_index = pd.read_csv(os.path.join("data", "Input", "nifty_eom.csv"))
    df_index["Date"] = pd.to_datetime(df_index["Date"])

    index_start = df_index[df_index["Date"] >= start_date].sort_values(by="Date").head(1)
    index_end = df_index[df_index["Date"] <= end_date].sort_values(by="Date", ascending=False).head(1)

    index_return = 0
    if not index_start.empty and not index_end.empty:
        index_start_value = index_start["Close"].values[0]
        index_end_value = index_end["Close"].values[0]
        index_return = ((index_end_value - index_start_value) / index_start_value) * 100

    return df_top_backtest, portfolio_return, index_return
