import streamlit as st
import os

st.set_page_config(layout="wide")

def read_markdown_file(markdown_file):
    with open(markdown_file, "r", encoding="utf-8") as file:
        return file.read()

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

content_map = {
    "SS_1 Report": os.path.join(REPORTS_DIR, "Report ss_1.md"),
}

st.title("Reports")

selected_report = st.selectbox("Select a report:", list(content_map.keys()))

if selected_report:
    markdown_file = content_map[selected_report]
    try:
        content = read_markdown_file(markdown_file)
        st.markdown(content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"File '{markdown_file}' not found. Please check the file path.")