import pandas as pd
import os
from pages.ss_scripts.ss1_scripts.returns_calculations import mf_returns_calculations

def get_top_funds(min_days, top_n_alpha, start_date, end_date, index_name):
     
    df_mf_raw = pd.read_csv(os.path.join("Data", "Input", "mf_eom.csv"))
    
    if index_name == "Nifty 50" :
        df_index_raw = pd.read_csv(os.path.join("Data", "Input", "nifty_eom.csv"))
    elif index_name == "Nifty 500" :
        df_index_raw = pd.read_csv(os.path.join("Data", "Input", "nifty500_eom.csv")) 

    df_mf = df_mf_raw[pd.to_datetime(df_mf_raw['nav_date'], dayfirst=True) <= pd.Timestamp(start_date)].copy()
    df_index = df_index_raw[pd.to_datetime(df_index_raw['Date'], dayfirst=True) <= pd.Timestamp(start_date)].copy()
    
    df = mf_returns_calculations(df_mf, df_index)
    
    start_date = pd.to_datetime(start_date, dayfirst=True)
    end_date = pd.to_datetime(end_date, dayfirst=True)

    df_filtered = df[df["Duration (Days)"] >= min_days]

    df_sorted = df_filtered.sort_values(by="Excess Return (%)", ascending=False)
    df_top_backtest = df_sorted.head(top_n_alpha)

    '''The following is for the cumulative return calculation of an equi weighted portfolio of the backtest funds held from the start to end date'''

    df_mf_nav = df_mf_raw
    df_mf_nav["nav_date"] = pd.to_datetime(df_mf_nav["nav_date"],dayfirst=True)

    fund_returns = []
    
    for fund in df_top_backtest['Fund Name']:
        fund_data = df_mf_nav[df_mf_nav['scheme_name'] == fund]

        # Get NAV at or after start_date
        mf_nav_start = fund_data[fund_data["nav_date"] >= start_date].sort_values(by="nav_date").head(1)
        # Get NAV at or before end_date
        mf_nav_end = fund_data[fund_data["nav_date"] <= end_date].sort_values(by="nav_date").tail(1)

        if not mf_nav_start.empty and not mf_nav_end.empty:
            mf_nav_start_value = mf_nav_start["nav"].values[0]
            mf_nav_end_value = mf_nav_end["nav"].values[0]
            fund_return = ((mf_nav_end_value - mf_nav_start_value) / mf_nav_start_value) * 100
            fund_returns.append(fund_return)

    portfolio_return = sum(fund_returns) / len(fund_returns) if fund_returns else 0

    '''The following is for the cumulative returns of the index in the same period that the equi weighted back test portfolio is held'''
   
    df_index = df_index_raw
    df_index["Date"] = pd.to_datetime(df_index["Date"],dayfirst=True)

    index_start = df_index[df_index["Date"] >= start_date].sort_values(by="Date").head(1)
    index_end = df_index[df_index["Date"] <= end_date].sort_values(by="Date", ascending=False).head(1)

    index_return = 0
    if not index_start.empty and not index_end.empty:
        index_start_value = index_start["Close"].values[0]
        index_end_value = index_end["Close"].values[0]
        index_return = ((index_end_value - index_start_value) / index_start_value) * 100

    return df_top_backtest, portfolio_return, index_return

#Function for backtest animation
def get_nav_history(selected_funds, start_date, end_date, index_name):
    
    df_mf_raw = pd.read_csv(os.path.join("Data", "Input", "mf_eom.csv"))
    
    if index_name == "Nifty 50" :
        df_index_raw = pd.read_csv(os.path.join("Data", "Input", "nifty_eom.csv"))
    elif index_name == "Nifty 500" :
        df_index_raw = pd.read_csv(os.path.join("Data", "Input", "nifty500_eom.csv")) 

    start_date = pd.to_datetime(start_date,dayfirst=True)
    end_date = pd.to_datetime(end_date,dayfirst=True)

    df_nav = df_mf_raw
    df_index = df_index_raw

    df_nav["nav_date"] = pd.to_datetime(df_nav["nav_date"],dayfirst=True)
    df_index["Date"] = pd.to_datetime(df_index["Date"],dayfirst=True)

    df_portfolio = df_nav[df_nav["scheme_name"].isin(selected_funds)]
    df_portfolio = df_portfolio[(df_portfolio["nav_date"] >= start_date) & (df_portfolio["nav_date"] <= end_date)]

    df_index = df_index[(df_index["Date"] >= start_date) & (df_index["Date"] <= end_date)][["Date", "Close"]]

    return df_portfolio, df_index