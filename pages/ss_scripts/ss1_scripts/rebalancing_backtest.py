import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from pages.ss_scripts.ss1_scripts.calculations import mf_returns_calculations

def validate_rebalancing(start_date, end_date, rebalance_freq):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    duration_days = (end_date - start_date).days

    # Minimum required duration based on frequency
    min_duration = {
        "Monthly": 30,
        "Quarterly": 90,
        "Semi-Annual": 180,
        "Annual": 365
    }

    if duration_days < min_duration[rebalance_freq]:
        return False, f"Time period is too short for {rebalance_freq} rebalancing. Choose a longer duration or lower frequency."
    return True, None

import pandas as pd
import os

import pandas as pd
import os

import pandas as pd
import os
from dateutil.relativedelta import relativedelta

def backtest_with_rebalancing(start_date, end_date, min_days, top_n_alpha, rebalance_freq):
    """
    Performs a backtest with periodic rebalancing and re-evaluation.

    Args:
        start_date (date): The start date of the backtesting period.
        end_date (date): The end date of the backtesting period.
        min_days (int): The minimum number of days a fund must have existed.
        top_n_alpha (int): The number of top funds to pick based on Excess Return (%).
        rebalance_freq (str): The rebalancing frequency ("Monthly", "Quarterly", "Semi-Annual", "Annual").

    Returns:
        tuple: (DataFrame, float, float, int, int) - A tuple containing:
            - DataFrame: A DataFrame of the top selected funds over time.
            - float: Portfolio return.
            - float: Index return.
            - int: Number of unique funds selected.
            - int: Number of rebalances performed.
    """

    # Load Mutual Fund & Index Data
    df_mf_raw = pd.read_csv(os.path.join("Data", "Input", "mf_eom.csv"))
    df_index_raw = pd.read_csv(os.path.join("Data", "Input", "nifty_eom.csv"))

    # Convert Dates to Datetime
    df_mf_raw["nav_date"] = pd.to_datetime(df_mf_raw["nav_date"], dayfirst=True)
    df_index_raw["Date"] = pd.to_datetime(df_index_raw["Date"], dayfirst=True)
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Initialize Backtest Variables
    current_date = start_date
    portfolio_value = 1000  # Initial Portfolio Value
    unique_funds = set()
    rebalancing_dates = []
    all_selected_funds = []

    # Define Rebalancing Frequency Mapping
    rebalance_map = {
        "Monthly": relativedelta(months=1),
        "Quarterly": relativedelta(months=3),
        "Semi-Annual": relativedelta(months=6),
        "Annual": relativedelta(years=1),
    }

    # Loop Through Rebalancing Intervals
    while current_date <= end_date:
        rebalancing_dates.append(current_date)

        # Get the closest available index NAV before or on the current date
        closest_index_date = df_index_raw[df_index_raw["Date"] <= current_date]["Date"].max()
        if pd.isna(closest_index_date):  # If no data available, skip this period
            current_date += rebalance_map[rebalance_freq]
            continue

        # Filter Mutual Fund Data up to Current Date
        df_mf = df_mf_raw[df_mf_raw["nav_date"] <= current_date].copy()

        # Run Calculations (This function should return the processed DataFrame)
        df = mf_returns_calculations(df_mf, df_index_raw)

        # Ensure the necessary column exists before filtering
        if "Duration (Days)" not in df.columns:
            raise KeyError("Expected 'Duration (Days)' column not found in processed DataFrame!")

        # Apply Selection Criteria
        df_filtered = df[df["Duration (Days)"] >= min_days]
        df_sorted = df_filtered.sort_values(by="Excess Return (%)", ascending=False)
        df_top_backtest = df_sorted.head(top_n_alpha)

        # Track Unique Funds Selected
        selected_funds = df_top_backtest["Fund Name"].tolist()
        unique_funds.update(selected_funds)
        all_selected_funds.append((current_date, selected_funds))

        # Allocate Portfolio Equally Among Selected Funds
        investment_per_fund = portfolio_value / top_n_alpha

        # Compute Portfolio Value at Next Rebalance Date
        next_rebalance_date = current_date + rebalance_map[rebalance_freq]
        df_mf_next = df_mf_raw[(df_mf_raw["nav_date"] > current_date) & (df_mf_raw["nav_date"] <= next_rebalance_date)]
        
        portfolio_value_new = 0
        for fund in selected_funds:
            df_fund = df_mf_next[df_mf_next["scheme_name"] == fund]

            # Get NAV at Next Rebalance Date (closest before or on next date)
            nav_start = df_mf_raw[(df_mf_raw["scheme_name"] == fund) & (df_mf_raw["nav_date"] <= current_date)]["nav"].max()
            nav_end = df_fund["nav"].max() if not df_fund.empty else nav_start  # Use same NAV if no new data

            if pd.notna(nav_start) and pd.notna(nav_end) and nav_start > 0:
                fund_return = (nav_end / nav_start) - 1
                portfolio_value_new += investment_per_fund * (1 + fund_return)
            else:
                portfolio_value_new += investment_per_fund  # Keep the same value if no new NAV

        # Update Portfolio Value
        portfolio_value = portfolio_value_new

        # Move to Next Rebalance Date
        current_date = next_rebalance_date

    index_start = df_index_raw[df_index_raw["Date"] >= start_date].sort_values(by="Date").head(1)
    index_end = df_index_raw[df_index_raw["Date"] <= end_date].sort_values(by="Date", ascending=False).head(1)

    index_return = 0
    if not index_start.empty and not index_end.empty:
        index_start_value = index_start["Close"].values[0]
        index_end_value = index_end["Close"].values[0]
        index_return = ((index_end_value - index_start_value) / index_start_value) * 100


    # Calculate Final Returns
    portfolio_return = ((portfolio_value / 1000) - 1) * 100  # % return
    index_return = ((index_end_value / index_start_value) - 1) * 100

    # Output Number of Unique Funds & Rebalances
    num_rebalances = len(rebalancing_dates) - 1
    unique_funds_count = len(unique_funds)

    # Convert Selected Funds Tracking to DataFrame
    df_selected_funds = pd.DataFrame(all_selected_funds, columns=["Rebalance Date", "Selected Funds"])

    return df_selected_funds, portfolio_return, index_return, unique_funds_count, num_rebalances