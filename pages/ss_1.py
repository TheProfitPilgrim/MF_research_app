import streamlit as st
import pandas as pd
import subprocess
import plotly.graph_objects as go
import os

from pages.ss_scripts.ss1_scripts import filtering_current
from pages.ss_scripts.ss1_scripts import filtering_backtest

# Setting width
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
    rebalance_yn = st.radio("Do you want to rebalancing?", ("Yes", "No"))

# Check if df_top_current is in session state
if "df_top_current" not in st.session_state:
    st.session_state.df_top_current = None  # Initialize as None

# Similarly for df_top_backtest
if "df_top_backtest" not in st.session_state:
    st.session_state.df_top_backtest = None

if st.button("Select"):
    if selection_mode == "Current":
        st.write("Running calculations...")

        # Run calculations_current.py
        subprocess.run(["python", os.path.join("ss_scripts", "ss1_scripts", "calculations_current.py")])

        # Filtering using get_top_funds function in filtering_current.py
        df_top_current = filtering_current.get_top_funds(min_days, top_n_alpha)

        # Store in session state
        st.session_state.df_top_current = df_top_current

    elif selection_mode == "Back Test" and rebalance_yn == "No":
        st.write("Running backtest calculations...")

        # Run calculations_backtest.py with start_date
        subprocess.run(["python", os.path.join("ss_scripts", "ss1_scripts", "calculations_backtest.py"), str(start_date)])
        
        portfolio_backtest_return = 0

        df_top_backtest, portfolio_backtest_return, index_backtest_return = filtering_backtest.get_top_funds(min_days, top_n_alpha, start_date, end_date)
        
        portfolio_backtest_return = round(portfolio_backtest_return,2)
        index_backtest_return = round(index_backtest_return,2)
        
        pf_to_index_bt_returns = portfolio_backtest_return / index_backtest_return
        pf_to_index_bt_returns = round(pf_to_index_bt_returns,2)
        
        # Store in session state
        st.session_state.df_top_backtest = df_top_backtest
        st.session_state.portfolio_backtest_return = portfolio_backtest_return
        st.session_state.index_backtest_return = index_backtest_return

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
    
   
    st.write(f'### Equi weighted portfolio return of the above table of funds if held till the end date = {portfolio_backtest_return} %')
    st.write(f'### Index returns in the same period {index_backtest_return} %')
    st.write(f'### Outperformed the index by {pf_to_index_bt_returns} times')
