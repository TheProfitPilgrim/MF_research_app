import streamlit as st

# App Title
st.title("Mutual Fund Backtesting App")

# Homepage - Selection System List
st.header("Select a Selection System")

# Create clickable selection system links
st.page_link("pages/ss_1.py", label="Selection System 1")

st.write("(More selection systems will be added here)")