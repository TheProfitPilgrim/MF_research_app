# pages/ss_scripts/n50_outlook_scripts/n50_outlook_calculations.py
import os
import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize

def load_nifty50outlook_corr(csv_path=None, date_col="Date", method="spearman"):
    if csv_path is None:
        csv_path = os.path.join("Data","india_data","nifty50outlook_data.csv")
    df = pd.read_csv(csv_path)
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
    if "Percentage Deviation from 14% CAGR" in df.columns and "cagr_dev" not in df.columns:
        df = df.rename(columns={"Percentage Deviation from 14% CAGR":"cagr_dev"})
    features = [c for c in ("P/E","P/B","CAPE","cagr_dev") if c in df.columns]
    fwd_a = ["fwd_1m","fwd_3m","fwd_6m","fwd_1y","fwd_2y","fwd_3y","fwd_4y","fwd_5y"]
    fwd_b = ["1 Month Forward Return","3 Month Forward Return","6 Month Forward Return","1 Year Forward Return","2 Year Forward Return","3 Year Forward Return","4 Year Forward Return","5 Year Forward Return"]
    targets = [c for c in fwd_a if c in df.columns]
    if not targets:
        targets = [c for c in fwd_b if c in df.columns]
    if not features or not targets:
        raise ValueError("Required features or forward return columns not found.")
    corr = df[features + targets].corr(method=method).loc[features, targets]
    return corr, features, targets, df

def freq_table_from_inputs(nifty_pe, nifty_pb, horizon_code, csv_path=None, cape=None, cagr_dev=None, score_window=0.25, bin_width_pct=10):
    if csv_path is None:
        csv_path = os.path.join("Data","india_data","nifty50outlook_data.csv")
    df = pd.read_csv(csv_path)
    if "Percentage Deviation from 14% CAGR" in df.columns and "cagr_dev" not in df.columns:
        df = df.rename(columns={"Percentage Deviation from 14% CAGR":"cagr_dev"})
    features_all = ["P/E","P/B","CAPE","cagr_dev"]
    features = [f for f in features_all if f in df.columns]
    targets_all = ["fwd_1m","fwd_3m","fwd_6m","fwd_1y","fwd_2y","fwd_3y","fwd_4y","fwd_5y"]
    targets = [t for t in targets_all if t in df.columns]
    df_mod = df.copy()
    for f in features:
        df_mod[f+"_wins"] = winsorize(df_mod[f].values, limits=[0.01,0.01])
    for f in features:
        w = df_mod[f+"_wins"]
        df_mod[f+"_std"] = (w - np.nanmean(w)) / np.nanstd(w, ddof=0)
    weights_by_target = {}
    for t in targets:
        corrs = {f: df_mod[[f+"_std", t]].corr(method="spearman").iloc[0,1] for f in features}
        s = {f: max(0.0, -corrs[f]) for f in features}
        tot = sum(s.values())
        weights_by_target[t] = {f: (s[f]/tot if tot>0 else 0.0) for f in features}
        df_mod["Score_"+t] = sum(weights_by_target[t][f]*df_mod[f+"_std"] for f in features)
    def _winsorize_scalar(x, arr):
        lo = np.nanquantile(arr, 0.01)
        hi = np.nanquantile(arr, 0.99)
        return min(max(float(x), lo), hi)
    def _zscore_scalar(x_wins, arr_wins):
        mu = np.nanmean(arr_wins)
        sd = np.nanstd(arr_wins, ddof=0)
        return (x_wins - mu)/sd if sd>0 else np.nan
    x_inputs = {}
    if "P/E" in features:
        x_inputs["P/E"] = float(nifty_pe)
    if "P/B" in features:
        x_inputs["P/B"] = float(nifty_pb)
    if "CAPE" in features:
        x_inputs["CAPE"] = float(cape) if cape is not None else float(df["CAPE"].iloc[-1])
    if "cagr_dev" in features:
        x_inputs["cagr_dev"] = float(cagr_dev) if cagr_dev is not None else float(df["cagr_dev"].iloc[-1])
    x_std = {}
    for f in features:
        arr = df[f].values
        xw = _winsorize_scalar(x_inputs[f], arr)
        hist_wins = winsorize(arr, limits=[0.01,0.01])
        x_std[f] = _zscore_scalar(xw, hist_wins)
    weights = weights_by_target.get(horizon_code, {})
    score_today = sum(weights.get(f,0.0)*x_std[f] for f in features)
    score_col = "Score_"+horizon_code
    if score_col not in df_mod.columns:
        return pd.DataFrame(columns=["Bin Range (%)","Frequency","Probability (%)"]), score_today, x_std, weights
    mask = df_mod[score_col].between(score_today - score_window, score_today + score_window)
    sub = df_mod.loc[mask, [horizon_code]].dropna().copy()
    if sub.empty:
        return pd.DataFrame(columns=["Bin Range (%)","Frequency","Probability (%)"]), score_today, x_std, weights
    vals = sub[horizon_code].values
    is_decimal = float(np.nanmedian(np.abs(vals))) <= 1.0
    ret_pct = vals*100.0 if is_decimal else vals
    lo = float(np.floor(ret_pct.min()/bin_width_pct)*bin_width_pct)
    hi = float(np.ceil(ret_pct.max()/bin_width_pct)*bin_width_pct)
    if hi == lo:
        hi = lo + bin_width_pct
    bins = np.arange(lo, hi+bin_width_pct, bin_width_pct, dtype=float)
    cats = pd.cut(ret_pct, bins=bins, right=False, include_lowest=True)
    freq = pd.Series(cats).value_counts().sort_index()
    total = int(freq.sum())
    table = pd.DataFrame({
        "Bin Range (%)":[f"[{int(i.left)}, {int(i.right)})" for i in freq.index],
        "Frequency":freq.values
    })
    table["Probability (%)"] = (table["Frequency"]/total)*100.0 if total>0 else 0.0
    total_row = pd.DataFrame({"Bin Range (%)":["Total"],"Frequency":[total],"Probability (%)":[100.0 if total>0 else 0.0]})
    table = pd.concat([table, total_row], ignore_index=True)
    return table, score_today, x_std, weights

def scatter_data_from_inputs(nifty_pe, nifty_pb, horizon_code, csv_path=None, cape=None, cagr_dev=None, score_window=0.25):
    if csv_path is None:
        csv_path = os.path.join("Data","india_data","nifty50outlook_data.csv")
    df = pd.read_csv(csv_path)
    if "Percentage Deviation from 14% CAGR" in df.columns and "cagr_dev" not in df.columns:
        df = df.rename(columns={"Percentage Deviation from 14% CAGR":"cagr_dev"})
    features = [f for f in ["P/E","P/B","CAPE","cagr_dev"] if f in df.columns]
    targets = [t for t in ["fwd_1m","fwd_3m","fwd_6m","fwd_1y","fwd_2y","fwd_3y","fwd_4y","fwd_5y"] if t in df.columns]
    df_mod = df.copy()
    for f in features:
        df_mod[f+"_wins"] = winsorize(df_mod[f].values, limits=[0.01,0.01])
    for f in features:
        w = df_mod[f+"_wins"]
        df_mod[f+"_std"] = (w - np.nanmean(w)) / np.nanstd(w, ddof=0)
    weights_by_target = {}
    for t in targets:
        corrs = {f: df_mod[[f+"_std", t]].corr(method="spearman").iloc[0,1] for f in features}
        s = {f: max(0.0, -corrs[f]) for f in features}
        tot = sum(s.values())
        weights_by_target[t] = {f: (s[f]/tot if tot>0 else 0.0) for f in features}
        df_mod["Score_"+t] = sum(weights_by_target[t][f]*df_mod[f+"_std"] for f in features)
    def _winsorize_scalar(x, arr):
        lo = np.nanquantile(arr, 0.01)
        hi = np.nanquantile(arr, 0.99)
        return min(max(float(x), lo), hi)
    def _zscore_scalar(x_wins, arr_wins):
        mu = np.nanmean(arr_wins)
        sd = np.nanstd(arr_wins, ddof=0)
        return (x_wins - mu)/sd if sd>0 else np.nan
    x_inputs = {}
    if "P/E" in features:
        x_inputs["P/E"] = float(nifty_pe)
    if "P/B" in features:
        x_inputs["P/B"] = float(nifty_pb)
    if "CAPE" in features:
        x_inputs["CAPE"] = float(cape) if cape is not None else float(df["CAPE"].iloc[-1])
    if "cagr_dev" in features:
        x_inputs["cagr_dev"] = float(cagr_dev) if cagr_dev is not None else float(df["cagr_dev"].iloc[-1])
    x_std = {}
    for f in features:
        arr = df[f].values
        xw = _winsorize_scalar(x_inputs[f], arr)
        hist_wins = winsorize(arr, limits=[0.01,0.01])
        x_std[f] = _zscore_scalar(xw, hist_wins)
    weights = weights_by_target.get(horizon_code, {})
    score_today = sum(weights.get(f,0.0)*x_std[f] for f in features)
    score_col = "Score_"+horizon_code
    if score_col not in df_mod.columns or horizon_code not in df_mod.columns:
        return pd.DataFrame(columns=["Score","Return (%)","In Window"]), score_today
    vals = df_mod[horizon_code].values
    is_decimal = float(np.nanmedian(np.abs(vals))) <= 1.0
    ret_pct = vals*100.0 if is_decimal else vals
    scatter_df = pd.DataFrame({
        "Score": df_mod[score_col].values,
        "Return (%)": ret_pct
    })
    scatter_df["In Window"] = scatter_df["Score"].between(score_today - score_window, score_today + score_window)
    if "Date" in df_mod.columns:
        scatter_df["Date"] = pd.to_datetime(df_mod["Date"], errors="coerce")
    return scatter_df, score_today
