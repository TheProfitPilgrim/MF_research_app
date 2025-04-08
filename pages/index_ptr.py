import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm 
from pages.ss_scripts.index_ptr_scripts.median_pe_model import calc_prob
from pages.ss_scripts.index_ptr_scripts.linear_reg_model import calc_prob_lr 
import scipy.stats as stats

st.set_page_config(layout="wide")

st.title("Index Direction Pointer")

st.markdown("### For Nifty 50 Only")
st.markdown("### Though it outputs some probability value, makes sense to consider only strong(>75% for up or down) outputs")

st.write("### Enter current index level :")
current_price = st.number_input("⤵️", min_value=1 , value=22000)

st.write("### Enter current index PE :")
current_pe = st.number_input("⤵️", min_value=1 , value=20)

selection_mode = ""
selection_mode = st.radio("Select Mode:", ("Median PE", "Simple Linear Regression"))    

if st.button("Flip") :
    if selection_mode == "Median PE":
        price_fair, x, prob_increasing, prob_decreasing, hist_deviations, a, loc, scale = calc_prob(current_price, current_pe)
        st.write(f"### \"Fair value\" is {price_fair :.2f}")
        st.write(f"### Deviation from fair value is {x : .2f} %")
        st.write(f"### Probability of index increasing: {prob_increasing*100:.2f} %")
        st.write(f"### Probability of index decreasing: {prob_decreasing*100:.2f} %")
        
        #graph
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

    elif selection_mode == "Simple Linear Regression" :
        pred_price, x, prob_increasing, prob_decreasing, data, best_params, best_name, crt_price, crt_earn, df = calc_prob_lr(current_price, current_pe)
        st.write(f"### Regression value is {pred_price :.2f}") 
        st.write(f"### How much regression value is away from current price  {x : .2f} %")
        current_x = x
        st.write(f"### Probability of index increasing: {prob_increasing:.2f} %")
        st.write(f"### Probability of index decreasing: {prob_decreasing:.2f} %")
        st.write(r"### $Regression \ Price_{current} = -343.73 + 23.3 \times Earnings_{current}$")
        st.write("")
        
        if isinstance(best_params, dict):
            shape_keys = [k for k in best_params if k not in ("loc", "scale")]
            shape_params = [float(best_params[k]) for k in shape_keys]
            loc = float(best_params.get("loc", 0))
            scale = float(best_params.get("scale", 1))

        else:
            params = [float(p) for p in best_params]
            *shape_params, loc, scale = params
        
        col1, col2 = st.columns(2)   
        #graph 1
        
        dist = getattr(stats, best_name)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(data, bins=30, density=True, color="skyblue", edgecolor="black", label="Original Data")
        x = np.linspace(min(data), max(data), 1000)
        y = dist.pdf(x, *shape_params, loc=loc, scale=scale)
        ax.plot(x, y, 'r-', label=f"Fitted {best_name} Distribution")
        ax.axvline(float(current_x), color='red', linestyle='--', label=f"Current Deviation: {float(current_x):.2f} %")
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.set_title(f"Best Fit: {best_name}")
        ax.legend()
        
        with col1:
            st.pyplot(fig)

        #graph 2

        plt.figure(figsize=(10, 6))
        plt.scatter(df['Earnings'], df['Close'], label='Actual data', color='grey', alpha=0.15)
        x_vals = df['Earnings']
        y_vals = -343.73 + 23.3 * x_vals
        plt.plot(x_vals, y_vals, color='red', label='Regression line')
        plt.scatter(crt_earn, crt_price, color='blue', s=100, label='Actual Point (current)', zorder=5)
        plt.scatter(crt_earn, pred_price, color='green', s=100, label='Regression Point', zorder=5)
        plt.plot([crt_earn, crt_earn], [crt_price, pred_price], color='black', linestyle='--')
        plt.xlabel('Earnings')
        plt.ylabel('Close')
        plt.title('Linear Regression: Earnings vs Close')
        plt.legend()
        
        with col2:
            st.pyplot(plt)

    else : 
            a = 1