import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

df = pd.read_csv(r"Data\\india_data\\nifty50_data.csv")
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df.sort_values("Date", ascending=True, inplace=True)

latest_date = df["Date"].max()
print(latest_date)
x = 0
look_fwd_days = 252


for index, row in df.iterrows():
    #while df["Date"].iloc[index + look_fwd_days] <= latest_date:
        #x += 0 
    print(index)

print(x)

