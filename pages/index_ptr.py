import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm 
from pages.ss_scripts.index_ptr_scripts.skew_norm_cdf import calc_prob

st.set_page_config(layout="wide")

st.title("Index Direction Pointer")

st.markdown("### For Nifty 50 Only")
st.markdown("### Though it outputs some probability value, makes sense to consider only strong(>75% for up or down) outputs")

st.write("### Enter current index level :")
current_price = st.number_input("⤵️", min_value=1 , value=22000)

st.write("### Enter current index PE :")
current_pe = st.number_input("⤵️", min_value=1 , value=20)    

if st.button("Flip"):
    price_fair, x, prob_increasing, prob_decreasing, hist_deviations, a, loc, scale = calc_prob(current_price, current_pe)
    st.write(f"\"Fair value\" is {price_fair :.2f}")
    st.write(f"Deviation from fair value is {x : .2f} %")
    st.write(f"Probability of index increasing: {prob_increasing*100:.2f} %")
    st.write(f"Probability of index decreasing: {prob_decreasing*100:.2f} %")
    fig, ax = plt.subplots(figsize=(8, 4))
    x_values = np.linspace(min(hist_deviations) - 10, max(hist_deviations) + 10, 1000)
    y_values = skewnorm.pdf(x_values, a, loc, scale)
    ax.plot(x_values, y_values, label="Skew-normal Distribution", color='blue', lw=2)
    ax.axvline(x, color='red', linestyle='--', label=f"Current Deviation: {x:.2f} %")
    ax.set_title("Distribution of Historical Deviations and Current Deviation")
    ax.set_xlabel("Deviation (%)")
    ax.set_ylabel("Density")
    ax.legend()
    st.pyplot(fig)