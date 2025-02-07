import pandas as pd 
import os

def get_top_funds(min_days, top_n_alpha):
    # Construct the path dynamically
    file_path = os.path.join("Data", "Output", "MF_calc.csv")

    # Load the generated MF_calc.csv
    df = pd.read_csv(file_path)

    # Filter based on minimum days
    df_filtered = df[df["Duration (Days)"] >= min_days]

    # Sort by Excess Return (%) in descending order
    df_sorted = df_filtered.sort_values(by="Excess Return (%)", ascending=False)

    # Select top N funds
    df_top_current = df_sorted.head(top_n_alpha)

    return df_top_current