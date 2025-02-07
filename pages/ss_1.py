import streamlit as st
import pandas as pd
import subprocess
import plotly.graph_objects as go
import os
from ss_scripts.ss1_scripts import *

#Setting width
st.set_page_config(layout="wide")

# App Title
st.title("Mutual Fund Backtesting App")

# SS_1 Page
st.title("Selection System 1")

st.header("Criteria:")

# User inputs for selection criteria
min_days = st.number_input("1. The fund must have existed for at least (days):", min_value=0, value=1000)
top_n_alpha = st.number_input("2. Sorted by descending all-time alpha to pick the top:", min_value=1, value=20)

# Selection mode
selection_mode = st.radio("Select Mode:", ("Current", "Back Test"))

if selection_mode == "Back Test":
    start_date = st.date_input("Backtest Start Date")
    end_date = st.date_input("Backtest End Date")
    rebalance_yn = st.radio("Do you want to rebalancing?",("Yes", "No"))

# Check if df_top_current is in session state
if "df_top_current" not in st.session_state:
    st.session_state.df_top_current = None  # Initialize as None

# similarly for df_top_backtest
if "df_top_backtest" not in st.session_state:
    st.session_state.df_top_backtest = None 

if st.button("Select"):
    if selection_mode == "Current":
        st.write("Running calculations...")

        # Path for calculations_current.py + running calculations_current
        calculations_current_path = os.path.join("ss_scripts", "ss1_scripts", "calculations_current.py")
        subprocess.run(["python", calculations_current_path])
        
        #filtering using the get_top_funds function in filtering_current.py 
        df_top_current = filtering_current.get_top_funds(min_days, top_n_alpha)

        # Store in session state
        st.session_state.df_top_current = df_top_current

    elif selection_mode == "Back Test" and rebalance_yn == "No":
        st.write("Running backtest calculations...")
        
        # we need to pass the start_date for running the calculations_backtest.py
        start_date_string = str(start_date)
        subprocess.run(["python", "calculations_backtest.py", start_date_string])
        
        df_top_backtest = filtering_backtest.get_top_funds(start_date, top_n_alpha)

        # Store in session state
        st.session_state.df_top_backtest = df_top_backtest
        
    elif selection_mode == "Back Test" and rebalance_yn == "Yes":
        print("Hello world")

# If df_top_current exists, display it
if st.session_state.df_top_current is not None:
    st.write("### Top Selected Funds")
    st.dataframe(st.session_state.df_top_current)

    # Visualization button
    if st.button("Visualize Excess Return"):
        df_top_current = st.session_state.df_top_current  # Get from session state
        fund_names = df_top_current["Fund Name"].tolist()
        final_values = df_top_current["Excess Return (%)"].values

        fig = go.Figure()

        # Add initial traces (all starting at 0)
        for fund in fund_names:
            fig.add_trace(go.Scatter(y=[0], x=[0], mode="lines", name=fund))

        # Create animation frames where all funds move together
        frames = []
        num_steps = 50  # Number of animation steps
        for step in range(1, num_steps + 1):
            frame_data = []
            for i, fund in enumerate(fund_names):
                y_val = (final_values[i] / num_steps) * step  # Gradual increase for each fund
                frame_data.append(go.Scatter(y=[0, y_val], x=[0, 1], mode="lines", name=fund))
            frames.append(go.Frame(data=frame_data))

        fig.frames = frames  # Assign animation frames

        fig.update_layout(
            updatemenus=[dict(type="buttons", showactive=False,
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None, dict(frame=dict(duration=50, redraw=True),
                                                             fromcurrent=True)])])],
            title="Mutual Fund Excess Return Animation",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis_title="Excess Return (%)"
        )

        st.plotly_chart(fig)
        
if st.session_state.df_top_backtest is not None:
        st.write("### Top Selected Funds")
        st.dataframe(st.session_state.df_top_backtest)