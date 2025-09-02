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
    features = [c for c in ("P/E","P/B","cagr_dev") if c in df.columns]
    fwd_a = ["fwd_1m","fwd_3m","fwd_6m","fwd_1y","fwd_2y","fwd_3y","fwd_4y","fwd_5y"]
    fwd_b = ["1 Month Forward Return","3 Month Forward Return","6 Month Forward Return","1 Year Forward Return","2 Year Forward Return","3 Year Forward Return","4 Year Forward Return","5 Year Forward Return"]
    targets = [c for c in fwd_a if c in df.columns]
    if not targets:
        targets = [c for c in fwd_b if c in df.columns]
    if not features or not targets:
        raise ValueError("Required features or forward return columns not found.")
    corr = df[features + targets].corr(method=method).loc[features, targets]
    return corr, features, targets, df

def compute_cagr_dev_today(nifty_value, csv_path=None, cagr_rate=0.135, date_col="Date"):
    if csv_path is None:
        csv_path = os.path.join("Data","india_data","nifty50outlook_data.csv")
    df = pd.read_csv(csv_path)
    if date_col not in df.columns:
        raise ValueError("Date column not found.")
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
    df = df.sort_values(date_col).reset_index(drop=True)
    close_candidates = ["Close","Nifty","NIFTY","Index","Price","Close Price","Nifty Value","Value"]
    close_col = next((c for c in close_candidates if c in df.columns), None)
    if close_col is None and "cagr_curve" not in df.columns:
        raise ValueError("No Close or cagr_curve column to anchor CAGR.")
    if close_col is not None:
        base_level = float(df[close_col].iloc[0])
    else:
        base_level = float(df["cagr_curve"].iloc[0])
    t0 = df[date_col].iloc[0]
    today = pd.Timestamp.today().normalize()
    yrs = max(0.0, (today - t0).days / 365.25)
    cagr_level_today = base_level * ((1.0 + float(cagr_rate)) ** yrs)
    dev_pct = ((float(nifty_value) - cagr_level_today) / cagr_level_today) * 100.0
    return float(dev_pct), float(cagr_level_today), today

def freq_table_from_inputs(nifty_pe, nifty_pb, horizon_code, csv_path=None, cagr_dev=None, score_window=0.25, bin_width_pct=10):
    if csv_path is None:
        csv_path = os.path.join("Data","india_data","nifty50outlook_data.csv")
    df = pd.read_csv(csv_path)
    if "Percentage Deviation from 14% CAGR" in df.columns and "cagr_dev" not in df.columns:
        df = df.rename(columns={"Percentage Deviation from 14% CAGR":"cagr_dev"})
    features_all = ["P/E","P/B","cagr_dev"]
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
    if "cagr_dev" in features:
        x_inputs["cagr_dev"] = float(cagr_dev) if cagr_dev is not None else float(df["cagr_dev"].iloc[-1]) if "cagr_dev" in df.columns else np.nan
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
        return pd.DataFrame(columns=["Bin Range (%)","Frequency","Probability (%)"]), score_today, x_std, weights, np.nan
    mask = df_mod[score_col].between(score_today - score_window, score_today + score_window)
    sub = df_mod.loc[mask, [horizon_code, "Date"]].dropna(subset=[horizon_code]).copy() if "Date" in df_mod.columns else df_mod.loc[mask, [horizon_code]].dropna().copy()
    if sub.empty:
        return pd.DataFrame(columns=["Bin Range (%)","Frequency","Probability (%)"]), score_today, x_std, weights, np.nan
    vals = sub[horizon_code].values
    is_decimal = float(np.nanmedian(np.abs(vals))) <= 1.0
    ret_pct = vals*100.0 if is_decimal else vals
    lo = float(np.floor(ret_pct.min()/bin_width_pct)*bin_width_pct)
    hi = float(np.ceil(ret_pct.max()/bin_width_pct)*bin_width_pct)
    if hi == lo:
        hi = lo + bin_width_pct
    bins = np.arange(lo, hi+bin_width_pct, bin_width_pct, dtype=float)
    cats = pd.cut(ret_pct, bins=bins, right=False, include_lowest=True)
    freq = cats.value_counts().sort_index()
    total = int(freq.sum())
    intervals = freq.index.tolist()
    mids = np.array([(iv.left + iv.right)/2.0 for iv in intervals], dtype=float)
    probs = freq.values.astype(float) / float(total) if total > 0 else np.zeros(len(freq), dtype=float)
    ev = float(np.sum(mids * probs)) if len(mids) > 0 else np.nan
    table = pd.DataFrame({
        "Bin Range (%)":[f"[{int(iv.left)}, {int(iv.right)})" for iv in intervals],
        "Frequency":freq.values,
        "Probability (%)":probs*100.0
    })
    total_row = pd.DataFrame({"Bin Range (%)":["Total"],"Frequency":[total],"Probability (%)":[100.0 if total>0 else 0.0]})
    table = pd.concat([table, total_row], ignore_index=True)
    return table, score_today, x_std, weights, ev

def scatter_data_from_inputs(nifty_pe, nifty_pb, horizon_code, csv_path=None, cagr_dev=None, score_window=0.25):
    if csv_path is None:
        csv_path = os.path.join("Data","india_data","nifty50outlook_data.csv")
    df = pd.read_csv(csv_path)
    if "Percentage Deviation from 14% CAGR" in df.columns and "cagr_dev" not in df.columns:
        df = df.rename(columns={"Percentage Deviation from 14% CAGR":"cagr_dev"})
    features = [f for f in ["P/E","P/B","cagr_dev"] if f in df.columns]
    targets = [t for t in ["fwd_1m","fwd_3m","fwd_6m","fwd_1y","fwd_2y","fwd_3y","fwd_4y","fwd_5y"] if t in df.columns]
    df_mod = df.copy()
    if "Date" in df_mod.columns:
        df_mod["Date"] = pd.to_datetime(df_mod["Date"], dayfirst=True, errors="coerce")
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
    if "cagr_dev" in features:
        x_inputs["cagr_dev"] = float(cagr_dev) if cagr_dev is not None else float(df["cagr_dev"].iloc[-1]) if "cagr_dev" in df.columns else np.nan
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
    scatter_df = pd.DataFrame({"Score": df_mod[score_col].values, "Return (%)": ret_pct})
    scatter_df["In Window"] = scatter_df["Score"].between(score_today - score_window, score_today + score_window)
    if "Date" in df_mod.columns:
        scatter_df["Date"] = pd.to_datetime(df_mod["Date"], errors="coerce")
    return scatter_df, score_today

def region_year_distribution_from_inputs(nifty_pe, nifty_pb, horizon_code, csv_path=None, cagr_dev=None, score_window=0.25, bucket_size=5, bucket_if_unique_years_gt=12):
    scatter_df, score_today = scatter_data_from_inputs(nifty_pe=nifty_pe, nifty_pb=nifty_pb, horizon_code=horizon_code, csv_path=csv_path, cagr_dev=cagr_dev, score_window=score_window)
    if "Date" not in scatter_df.columns or scatter_df.empty:
        return pd.DataFrame(columns=["Period","Count","Percent (%)"])
    sub = scatter_df.loc[scatter_df["In Window"]].dropna(subset=["Date"]).copy()
    if sub.empty:
        return pd.DataFrame(columns=["Period","Count","Percent (%)"])
    sub["Year"] = sub["Date"].dt.year.astype(int)
    uniq_years = sub["Year"].nunique()
    if uniq_years > bucket_if_unique_years_gt:
        y = sub["Year"].astype(int)
        start = (y // bucket_size) * bucket_size
        end = start + bucket_size - 1
        sub["Period"] = start.astype(str) + "-" + end.astype(str)
        grp = sub.groupby("Period", as_index=False).size().rename(columns={"size":"Count"})
    else:
        grp = sub.groupby("Year", as_index=False).size().rename(columns={"size":"Count"})
        grp["Period"] = grp["Year"].astype(str)
        grp = grp[["Period","Count"]]
    total = int(grp["Count"].sum())
    grp["Percent (%)"] = (grp["Count"] / total * 100.0) if total > 0 else 0.0
    grp = grp.sort_values("Period").reset_index(drop=True)
    return grp