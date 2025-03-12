import streamlit as st
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
    price_fair, x, prob_increasing, prob_decreasing = calc_prob(current_price, current_pe)
    st.write(f"\"Fair value\" is {price_fair :.2f}")
    st.write(f"Deviation from fair value is {x : .2f} %")
    st.write(f"Probability of index increasing: {prob_increasing*100:.2f} %")
    st.write(f"Probability of index decreasing: {prob_decreasing*100:.2f} %")