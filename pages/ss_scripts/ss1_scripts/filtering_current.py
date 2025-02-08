import pandas as pd
import os

df = pd.read_csv(os.path.join("Data", "Output", "MF_calc_current.csv"))

def get_top_funds(min_days, top_n_alpha):
    # Filter based on minimum days
    df_filtered = df[df["Duration (Days)"] >= min_days]

    # Sort by Excess Return (%) in descending order
    df_sorted = df_filtered.sort_values(by="Excess Return (%)", ascending=False)

    # Select top N funds
    return df_sorted.head(top_n_alpha)