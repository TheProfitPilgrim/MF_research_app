import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pages.ss_scripts.ss1_scripts import rebalancing_backtest_ss1
from pages.ss_scripts.ss1_scripts import filtering_current_ss1
from pages.ss_scripts.ss1_scripts import filtering_backtest_ss1

st.set_page_config(layout="wide")
st.title("Mutual Fund Backtesting App")
st.title("Selection System 1")
st.header("Selection Criteria:")
st.markdown('&nbsp;')

st.write("### Minimum time since inception for the fund (in days)")
min_days = st.number_input("⤵️", min_value=0, value=1000)
st.write("### Enter the number of funds you want in the portfolio")
top_n_alpha = st.number_input("⤵️", min_value=1, value=20)

selection_mode = st.radio("Select Mode:", ("Current", "Back Test"))

if selection_mode == "Back Test":

    start_date = st.date_input("Backtest Start Date")
    end_date = st.date_input("Backtest End Date")
    rebalance_yn = st.radio("Do you want rebalancing?", ("Yes", "No"))
    
    if rebalance_yn == "Yes":
        rebalance_freq = st.selectbox("Rebalancing Frequency", ["Quarterly", "Semi-Annual", "Annual"])
        for key in list(st.session_state.keys()): 
            if key not in ["all_pfs", "pf_bt_yes_return", "index_return", "num_rebalances"]:
                del st.session_state[key]
    else:
        for key in list(st.session_state.keys()): 
            if key not in ["df_top_backtest","pf_bt_no_return","index_backtest_return"]:
                del st.session_state[key]

else:
   for key in list(st.session_state.keys()): 
    if key != "df_top_current":
        del st.session_state[key]

if st.button("Select"):
    if selection_mode == "Current":
        st.write("Fetching current portfolio...")
        
        df_top_current = filtering_current_ss1.get_top_funds(min_days, top_n_alpha)
        
        st.session_state.df_top_current = df_top_current

    elif selection_mode == "Back Test" and rebalance_yn == "No":
        st.write("Running backtest calculations...")

        df_top_backtest, pf_bt_no_return, index_backtest_return = filtering_backtest_ss1.get_top_funds(min_days, top_n_alpha, start_date, end_date)
        
        pf_bt_no_return = round(pf_bt_no_return,2)
        index_backtest_return = round(index_backtest_return,2)
        
        if index_backtest_return!=0:
            pf_to_index_bt_returns = pf_bt_no_return / index_backtest_return
            pf_to_index_bt_returns = round(pf_to_index_bt_returns,2)
        else:
            st.write("### Please check the start and end dates again")

        st.session_state.df_top_backtest = df_top_backtest
        st.session_state.pf_bt_no_return = pf_bt_no_return
        st.session_state.index_backtest_return = index_backtest_return

    elif selection_mode == "Back Test" and rebalance_yn == "Yes":

        is_valid, error_msg = rebalancing_backtest_ss1.validate_rebalancing(start_date, end_date, rebalance_freq)
        
        if not is_valid:
            st.error(error_msg)
        else:
            st.write("Running backtest with rebalancing calculations...")

            all_pfs, pf_bt_yes_return, index_return, num_rebalances = rebalancing_backtest_ss1.backtest_with_rebalancing(start_date, end_date, min_days, top_n_alpha, rebalance_freq)
        
            st.session_state.all_pfs = all_pfs
            st.session_state.pf_bt_yes_return = pf_bt_yes_return
            st.session_state.index_return = index_return
            st.session_state.num_rebalances = num_rebalances
            

if "df_top_current" in st.session_state:
    st.write("### Current Top Funds")
    st.dataframe(st.session_state.df_top_current)
    
    if st.button("Visualize Excess Return"):
        df_top_current = st.session_state.df_top_current 

        # Histogram of Excess Returns
        fig = px.histogram(df_top_current, x="Excess Return (%)", nbins=20, 
                        title="Distribution of Excess Returns",
                        labels={"Excess Return (%)": "Excess Return (%)", "count": "Number of Funds"},
                        marginal="box", 
                        opacity=0.75,)
        fig.update_layout(
            bargap = 0.25,
            xaxis_title="Excess Return (%)",
            yaxis_title="Number of Funds" 
        )

        st.plotly_chart(fig)     

if "df_top_backtest" in st.session_state:
    st.write(f"### Portfolio formed on {start_date} and held till {end_date}")
    st.dataframe(st.session_state.df_top_backtest)
    
    if "pf_bt_no_return" in st.session_state:
        pf_bt_no_return = st.session_state.pf_bt_no_return
        index_backtest_return = st.session_state.index_backtest_return
        pf_to_index_bt_returns = round(pf_bt_no_return / index_backtest_return, 2)

        st.write(f'### Equi weighted portfolio return of the above table of funds if held till the end date = {pf_bt_no_return} %')
        st.write(f'### Index returns in the same period {index_backtest_return} %')
        st.write(f'### Outperformed the index by {pf_to_index_bt_returns} times')
    else:
        st.write("⚠️ No backtest results available yet. Please click 'Select' to run the backtest.")

    if st.button("Visualize Backtest Performance"):

        # Get NAV history for selected funds & index
        df_top_backtest = st.session_state.df_top_backtest
        df_portfolio, df_index = filtering_backtest_ss1.get_nav_history(df_top_backtest["Fund Name"].tolist(), start_date, end_date)

        # Normalize to ₹1000 at start_date
        df_index["Index Value"] = (df_index["Close"] / df_index["Close"].iloc[0]) * 1000
        df_portfolio["NAV Normalized"] = df_portfolio.groupby("scheme_name")["nav"].transform(lambda x: (x / x.iloc[0]) * 1000)

        # Average the normalized NAVs for portfolio
        df_portfolio_grouped = df_portfolio.groupby("nav_date")["NAV Normalized"].mean().reset_index()

        # Ensure correct column names
        df_portfolio_grouped.rename(columns={"nav_date": "Date", "NAV Normalized": "Portfolio Value"}, inplace=True)
        df_index.rename(columns={"Date": "Date", "Index Value": "Index Value"}, inplace=True)

        # Merge data
        df_combined = pd.merge(df_portfolio_grouped, df_index[["Date", "Index Value"]], on="Date", how="outer").sort_values("Date")

        # Convert Date to string for animation
        df_combined["Date"] = df_combined["Date"].dt.strftime("%Y-%m-%d")

        # Create base figure
        fig = go.Figure()

        # Add initial traces (first frame)
        fig.add_trace(go.Scatter(x=[df_combined["Date"].iloc[0]], y=[df_combined["Portfolio Value"].iloc[0]], 
                                mode="lines", name="Portfolio", line=dict(color="green")))
        
        fig.add_trace(go.Scatter(x=[df_combined["Date"].iloc[0]], y=[df_combined["Index Value"].iloc[0]], 
                                mode="lines", name="Index", line=dict(color="blue")))

        # Create animation frames
        frames = []
        for i in range(1, len(df_combined)):
            frame = go.Frame(
                data=[
                    go.Scatter(x=df_combined["Date"][:i], y=df_combined["Portfolio Value"][:i], mode="lines", name="Portfolio", line=dict(color="green")),
                    go.Scatter(x=df_combined["Date"][:i], y=df_combined["Index Value"][:i], mode="lines", name="Index", line=dict(color="blue"))
                ],
                name=str(i),
            )
            frames.append(frame)

        fig.update(frames=frames)

        # Add play/pause buttons
        fig.update_layout(
            title="Portfolio vs Index Backtest Performance (₹1000 Base)",
            xaxis_title="Date",
            yaxis_title="Investment Value (₹)",
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]
                        )
                    ]
                )
            ]
        )

        # Show in Streamlit
        st.plotly_chart(fig)

if "pf_bt_yes_return" in st.session_state:
    
    st.subheader("Backtest Results with Rebalancing")
    st.write(f"### Portfolio Return: {st.session_state.pf_bt_yes_return:.2f}%")
    st.write(f"### Index Return: {st.session_state.index_return:.2f}%")
    st.write(f"### Number of Rebalances: {st.session_state.num_rebalances}")
    
    st.write("### Portfolio Rebalancing History")
    for index, row in st.session_state.all_pfs.iterrows():
        with st.expander(f"View Portfolio for {row['Rebalance Date'].date()}"):
            st.write(row["Portfolio"])