# pages/n50_outlook.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pages.ss_scripts.n50_outlook_scripts.n50_outlook_calculations import load_nifty50outlook_corr, freq_table_from_inputs, scatter_data_from_inputs

st.set_page_config(page_title="N50 Outlook", layout="wide")
st.title("Nifty 50 Outlook")

timeframe_options = [
    ("1 Month", "fwd_1m"),
    ("3 Months", "fwd_3m"),
    ("6 Months", "fwd_6m"),
    ("1 Year", "fwd_1y"),
    ("2 Years", "fwd_2y"),
    ("3 Years", "fwd_3y"),
    ("4 Years", "fwd_4y"),
    ("5 Years", "fwd_5y"),
]

with st.form("n50_inputs"):
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        nifty_value = st.number_input("Current Nifty value", min_value=0.0, value=25000.0, step=1.0, format="%.2f")
    with c2:
        nifty_pe = st.number_input("Current Nifty P/E", min_value=0.0, value=22.0, step=0.1, format="%.2f")
    with c3:
        nifty_pb = st.number_input("Current Nifty P/B", min_value=0.0, value=3.50, step=0.01, format="%.2f")
    with c4:
        horizon_label = st.selectbox("Timeframe", [lbl for lbl, _ in timeframe_options], index=3)
    submitted = st.form_submit_button("Submit")

if submitted:
    horizon_code = dict(timeframe_options)[horizon_label]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nifty", f"{nifty_value:,.2f}")
    c2.metric("P/E", f"{nifty_pe:.2f}")
    c3.metric("P/B", f"{nifty_pb:.2f}")
    c4.metric("Horizon", horizon_label)
    corr, features, targets, df = load_nifty50outlook_corr()
    absmax = float(corr.abs().max().max())
    styler = corr.style.format("{:.2f}").background_gradient(cmap="RdBu", vmin=-absmax, vmax=absmax)
    st.subheader("Feature vs Forward Returns (Correlation)")
    st.dataframe(styler, use_container_width=True)
    st.subheader("Forward Return Probability Table")
    table, score_today, x_std, weights = freq_table_from_inputs(nifty_pe=nifty_pe, nifty_pb=nifty_pb, horizon_code=horizon_code)
    st.dataframe(table.style.format({"Probability (%)":"{:.2f}"}), use_container_width=True)
    st.subheader("Historical Scatter: Score vs Forward Return")
    scatter_df, score_today_scatter = scatter_data_from_inputs(nifty_pe=nifty_pe, nifty_pb=nifty_pb, horizon_code=horizon_code)
    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(scatter_df.loc[~scatter_df["In Window"], "Score"], scatter_df.loc[~scatter_df["In Window"], "Return (%)"], alpha=0.35)
    ax.scatter(scatter_df.loc[scatter_df["In Window"], "Score"], scatter_df.loc[scatter_df["In Window"], "Return (%)"], alpha=0.9)
    ax.axvspan(score_today_scatter - 0.25, score_today_scatter + 0.25, alpha=0.15)
    ax.axvline(score_today_scatter, linestyle="--")
    ax.set_xlabel("Score")
    ax.set_ylabel("Forward Return (%)")
    ax.set_title(f"Score vs {horizon_label} Return")
    st.pyplot(fig, use_container_width=True)
