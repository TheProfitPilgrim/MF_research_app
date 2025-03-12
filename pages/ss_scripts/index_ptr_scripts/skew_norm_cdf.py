import pandas as pd
from  scipy.stats import skewnorm 
import os

def calc_prob(current_price, current_pe):
    
    df = pd.read_csv(os.path.join("Data", "india_data", "nifty50_data.csv"))
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df.sort_values("Date", inplace=True)
    
    pe_median_latest = df['PE'].median()
    
    hist_deviations = []
    for i in range (len(df)):
        pe_median = df['PE'].median()
        price_fair = pe_median * df["Earnings"].tail(1).iloc[0]
        deviation_price = ( df["Close"].tail(1).iloc[0] - price_fair) / price_fair * 100
        hist_deviations.append(round(deviation_price,2))
        df = df.iloc[:-1]
    
    current_earnings = current_price / current_pe

    price_fair = pe_median_latest*current_earnings
    x = float((current_price - price_fair) / price_fair * 100)

    parameters = skewnorm.fit(hist_deviations)
    print(type(parameters))
    a, loc, scale = parameters
    cdf = skewnorm.cdf(x, a , loc=loc, scale=scale)

    prob_increasing = 1 - cdf

    prob_decreasing = cdf

    return price_fair, x, prob_increasing, prob_decreasing