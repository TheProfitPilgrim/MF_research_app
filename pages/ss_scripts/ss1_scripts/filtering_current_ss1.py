import pandas as pd
import os
from pages.ss_scripts.ss1_scripts.returns_calculations import mf_returns_calculations

def get_top_funds(min_days, top_n_alpha, index_name):
    
    df_mf = pd.read_csv(os.path.join("Data", "Input", "mf_eom.csv"))
    
    if index_name == "Nifty 50" :
        df_index = pd.read_csv(os.path.join("Data", "Input", "nifty_eom.csv"))
    elif index_name == "Nifty 500" :
        df_index = pd.read_csv(os.path.join("Data", "Input", "nifty500_eom.csv"))
        
    df = mf_returns_calculations(df_mf, df_index)
   
    df_filtered = df[df["Duration (Days)"] >= min_days]

    df_sorted = df_filtered.sort_values(by="Excess Return (%)", ascending=False)

    return df_sorted.head(top_n_alpha)