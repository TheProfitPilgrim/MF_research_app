# pages/n50_outlook.py
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pages.ss_scripts.n50_outlook_scripts.n50_outlook_calculations import load_nifty50outlook_corr, freq_table_from_inputs, scatter_data_from_inputs, compute_cagr_dev_today, region_year_distribution_from_inputs

st.set_page_config(page_title="N50 Outlook", layout="wide")
st.title("Index Outlook")

index_options = [
    ("Nifty 50", os.path.join("Data","india_data","nifty50outlook_data.csv")),
    ("Nifty Smallcap 100", os.path.join("Data","india_data","niftysmallcap100outlook_data.csv")),
]

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

with st.form("inputs"):
    r1c1, r1c2 = st.columns([1,3])
    with r1c1:
        index_label = st.selectbox("Index", [lbl for lbl, _ in index_options], index=0)
    csv_path = dict(index_options)[index_label]
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1:
        idx_value = st.number_input(f"Current index value", min_value=0.0, value=25000.0, step=1.0, format="%.2f")
    with c2:
        pe = st.number_input("Current P/E", min_value=0.0, value=22.0, step=0.1, format="%.2f")
    with c3:
        pb = st.number_input("Current P/B", min_value=0.0, value=3.50, step=0.01, format="%.2f")
    with c4:
        horizon_label = st.selectbox("Timeframe", [lbl for lbl, _ in timeframe_options], index=3)
    with c5:
        score_window = st.number_input("Score window (±)", min_value=0.05, max_value=2.0, value=0.50, step=0.05, format="%.2f")
    submitted = st.form_submit_button("Submit")

if submitted:
    horizon_code = dict(timeframe_options)[horizon_label]
    dev_pct, cagr_level_today, today_ts = compute_cagr_dev_today(nifty_value=idx_value, csv_path=csv_path)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Index", index_label)
    m2.metric("Level", f"{idx_value:,.2f}")
    m3.metric("P/E", f"{pe:.2f}")
    m4.metric("P/B", f"{pb:.2f}")
    m5.metric("13.5% CAGR level", f"{cagr_level_today:,.2f}")
    m6.metric("Deviation vs CAGR (%)", f"{dev_pct:.2f}")
    corr, features, targets, df = load_nifty50outlook_corr(csv_path=csv_path)
    absmax = float(corr.abs().max().max())
    styler = corr.style.format("{:.2f}").background_gradient(cmap="RdBu", vmin=-absmax, vmax=absmax)
    st.subheader("Feature vs Forward Returns (Correlation)")
    st.dataframe(styler, use_container_width=True)
    st.subheader("Score Equation")
    table, score_today, x_std, weights, expected_value = freq_table_from_inputs(
        nifty_pe=pe,
        nifty_pb=pb,
        horizon_code=horizon_code,
        csv_path=csv_path,
        cagr_dev=dev_pct,
        score_window=score_window
    )
    ordered_feats = [f for f in ["P/E","P/B","cagr_dev"] if f in weights]
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
        nifty_pe=pe,
        nifty_pb=pb,
        horizon_code=horizon_code,
        csv_path=csv_path,
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
    ax.set_title(f"{index_label}: Score vs {horizon_label} Return")
    st.pyplot(fig, use_container_width=True)
    st.subheader("Where Do The Analogs Come From?")
    year_dist = region_year_distribution_from_inputs(
        nifty_pe=pe,
        nifty_pb=pb,
        horizon_code=horizon_code,
        csv_path=csv_path,
        cagr_dev=dev_pct,
        score_window=score_window,
        bucket_size=5,
        bucket_if_unique_years_gt=12
    )
    st.dataframe(year_dist.style.format({"Percent (%)":"{:.2f}"}), use_container_width=True)
    if not year_dist.empty:
        fig2, ax2 = plt.subplots(figsize=(8,4))
        ax2.bar(year_dist["Period"], year_dist["Percent (%)"])
        ax2.set_xlabel("Period")
        ax2.set_ylabel("Percent (%)")
        ax2.set_title("Distribution of Matching Samples by Period")
        plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
        st.pyplot(fig2, use_container_width=True)