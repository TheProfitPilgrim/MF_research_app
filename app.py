import streamlit as st

st.title("Mutual Fund Backtesting App")

st.header("Select a Selection System")

st.page_link("pages/ss_1.py", label="Selection System 1")

st.page_link("pages/index_ptr.py", label = "Index Direction Pointer")

st.write("(More selection systems will be added here)")