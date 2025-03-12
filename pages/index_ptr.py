import streamlit as st
import pandas as pd
from  scipy.stats import skewnorm 

st.set_page_config(layout="wide")

st.title("Index Direction Pointer")

st.markdown("### For Nifty 50 Only")
st.markdown("### Though it outputs some probability value, makes sense to consider only strong(>75% for up or down) outputs")

st.write("### Enter current index level :")
current_price = st.number_input("⤵️", min_value=1 , value=22000)

st.write("### Enter current index PE :")
current_pe = st.number_input("⤵️", min_value=1 , value=20)

def calc_prob(current_in_price, current_in_pe):
    
    df = pd.read_csv(r"Data\\india_data\\nifty50_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df.sort_values("Date", inplace=True)
    
    pe_median_latest = df['PE'].median()
    
    hist_deviations = []
    for i in range (len(df)):
        pe_median = df['PE'].median()
        price_fair = pe_median * df["Earnings"].tail(1).iloc[0]
        date = df["Date"].tail(1).iloc[0]
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
    

if st.button("Flip"):
    price_fair, x, prob_increasing, prob_decreasing = calc_prob(current_price, current_pe)
    st.write(f"\"Fair value\" is {price_fair :.2f}")
    st.write(f"Deviation from fair value is {x : .2f} %")
    st.write(f"Probability of index increasing: {prob_increasing*100:.2f} %")
    st.write(f"Probability of index decreasing: {prob_decreasing*100:.2f} %")