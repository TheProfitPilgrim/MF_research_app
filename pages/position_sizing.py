import streamlit as st
import pandas as pd 
from pages.ss_scripts.position_sizing_scripts.position_calculations import max_buyable_calc, risk_determination

st.set_page_config(layout="wide")

st.title("Position Sizing")

col1, col2 = st.columns(2)

with col1:
    st.write("### Period for stock expected return (years)")
    period = st.slider("",key="1",min_value=1, max_value=10, value=3, step=1)
    st.write("### Benchmark expected return (%) (from CMP)")
    bench_exp_ret = st.slider("",key="2",min_value=0, max_value=100, value=15, step=5)
    st.write("### Stock expected return (%)")
    stk_exp_ret = st.slider("",key="3",min_value=0, max_value=100, value=25, step=5)
    st.write("### CMP (₹)")
    cmp = st.slider("",key="4",min_value=0, max_value=1000, value=100, step=5)
    max_buyable = max_buyable_calc(period, bench_exp_ret, stk_exp_ret, cmp)
    
    st.write("### Equity Exposure (Lakhs)")
    eq_exposure = st.slider("",key="5",min_value=10, max_value=500, value=100, step=10)*100000
    st.write("### Risk per trade (%)")
    risk_per_trade = st.slider("",key="6",min_value=1.0, max_value=25.0, value=1.0, step=0.5)
    st.write("### Stop Loss (₹)")
    sl = st.slider("",key="7",min_value=0, max_value=1000, value=80, step=5)
    if sl >= cmp:
        st.error('Stop Loss (SL) must be less than Current Market Price (CMP). Please adjust the SL.')
    max_pos = risk_determination(eq_exposure, risk_per_trade, sl, cmp)    
    
with col2:
    st.write("### 1. Green indicates cmp < max buyable, red otherwise (red only when benchmark expected > stk expected)")
    if max_buyable > cmp:
        st.write(f"### :green[Max buyable price : ₹{max_buyable}]")
    else:
        st.write(f"### :red[Max buyable price : ₹{max_buyable}]")

    st.write(f"### 2. Maximum Initial Buy Allowed = {max_pos} shares")

    st.write("### Trade")

    qty_to_buy = st.number_input("Quantity to buy")
    price_of_buy = st.number_input("Price of buy")

    if 'tradebook' not in st.session_state:
        st.session_state.tradebook = pd.DataFrame(columns=['Sno.', 'Allowed Qty', 'Qty bought', 'Price', 'Value'])
    if 'sno_counter' not in st.session_state:
        st.session_state.sno_counter = 0

    def trade_details():
        current_sno = st.session_state.sno_counter + 1
        st.session_state.sno_counter = current_sno

        new_row_data = {
            'Sno.': current_sno,
            'Allowed Qty': max_pos,
            'Qty bought': qty_to_buy,
            'Price': price_of_buy,
            'Value': qty_to_buy * price_of_buy
        }
        new_row_df = pd.DataFrame([new_row_data])
        st.session_state.tradebook = pd.concat([st.session_state.tradebook, new_row_df], ignore_index=True)

    if st.button("Add"):
        trade_details()

    st.dataframe(st.session_state.tradebook, hide_index=True)
    
    