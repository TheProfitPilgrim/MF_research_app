# pages/n50_outlook.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pages.ss_scripts.n50_outlook_scripts.n50_outlook_calculations import load_nifty50outlook_corr, freq_table_from_inputs, scatter_data_from_inputs, compute_cagr_dev_today

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
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1:
        nifty_value = st.number_input("Current Nifty value", min_value=0.0, value=25000.0, step=1.0, format="%.2f")
    with c2:
        nifty_pe = st.number_input("Current Nifty P/E", min_value=0.0, value=22.0, step=0.1, format="%.2f")
    with c3:
        nifty_pb = st.number_input("Current Nifty P/B", min_value=0.0, value=3.50, step=0.01, format="%.2f")
    with c4:
        horizon_label = st.selectbox("Timeframe", [lbl for lbl, _ in timeframe_options], index=3)
    with c5:
        score_window = st.number_input("Score window (±)", min_value=0.05, max_value=2.0, value=0.50, step=0.05, format="%.2f")
    submitted = st.form_submit_button("Submit")

if submitted:
    horizon_code = dict(timeframe_options)[horizon_label]
    dev_pct, cagr_level_today, today_ts = compute_cagr_dev_today(nifty_value=nifty_value)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Nifty", f"{nifty_value:,.2f}")
    c2.metric("P/E", f"{nifty_pe:.2f}")
    c3.metric("P/B", f"{nifty_pb:.2f}")
    c4.metric("Horizon", horizon_label)
    c5.metric("13.5% CAGR level (today)", f"{cagr_level_today:,.2f}")
    c6.metric("Deviation vs CAGR (%)", f"{dev_pct:.2f}")
    corr, features, targets, df = load_nifty50outlook_corr()
    absmax = float(corr.abs().max().max())
    styler = corr.style.format("{:.2f}").background_gradient(cmap="RdBu", vmin=-absmax, vmax=absmax)
    st.subheader("Feature vs Forward Returns (Correlation)")
    st.dataframe(styler, use_container_width=True)
    st.subheader("Score Equation")
    table, score_today, x_std, weights, expected_value = freq_table_from_inputs(
        nifty_pe=nifty_pe,
        nifty_pb=nifty_pb,
        horizon_code=horizon_code,
        cagr_dev=dev_pct,
        score_window=score_window
    )
    ordered_feats = [f for f in ["P/E","P/B","CAPE","cagr_dev"] if f in weights]
    nonzero_feats = [f for f in ordered_feats if weights.get(f,0) != 0]
    if not nonzero_feats:
        nonzero_feats = ordered_feats
    sym = " + ".join([f"{weights.get(f,0):.2f}*{f}_std" for f in nonzero_feats])
    num = " + ".join([f"{weights.get(f,0):.2f}*{x_std.get(f,float('nan')):.2f}" for f in nonzero_feats])
    st.code(f"Score = {sym}")
    st.code(f"Score = {num} = {score_today:.2f}")
    st.subheader("Forward Return Probability Table")
    st.dataframe(table.style.format({"Probability (%)":"{:.2f}"}), use_container_width=True)
    st.metric("Expected Return (%)", f"{(expected_value if pd.notna(expected_value) else float('nan')):.2f}")
    st.subheader("Historical Scatter: Score vs Forward Return")
    scatter_df, score_today_scatter = scatter_data_from_inputs(
        nifty_pe=nifty_pe,
        nifty_pb=nifty_pb,
        horizon_code=horizon_code,
        cagr_dev=dev_pct,
        score_window=score_window
    )
    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(scatter_df.loc[~scatter_df["In Window"], "Score"], scatter_df.loc[~scatter_df["In Window"], "Return (%)"], alpha=0.35)
    ax.scatter(scatter_df.loc[scatter_df["In Window"], "Score"], scatter_df.loc[scatter_df["In Window"], "Return (%)"], alpha=0.9)
    ax.axvspan(score_today_scatter - score_window, score_today_scatter + score_window, alpha=0.15)
    ax.axvline(score_today_scatter, linestyle="--")
    ax.set_xlabel("Score")
    ax.set_ylabel("Forward Return (%)")
    ax.set_title(f"Score vs {horizon_label} Return")
    st.pyplot(fig, use_container_width=True)