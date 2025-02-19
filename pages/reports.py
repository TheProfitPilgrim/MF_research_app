import streamlit as st
import os

# Function to read markdown files
def read_markdown_file(markdown_file):
    with open(markdown_file, "r", encoding="utf-8") as file:
        return file.read()

# Define the correct path to the reports folder
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

# Mapping selection options to markdown files
content_map = {
    "SS_1 Report": os.path.join(REPORTS_DIR, "Report ss_1.md"),
    "Ideal Rebalancing Frequency": os.path.join(REPORTS_DIR, "Ideal rebalancing frequency.md"),
}

st.title("Markdown Viewer")

# Selection box for choosing a markdown file
selected_report = st.selectbox("Select a section:", list(content_map.keys()))

# Display the selected markdown content
if selected_report:
    markdown_file = content_map[selected_report]
    try:
        content = read_markdown_file(markdown_file)
        st.markdown(content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"File '{markdown_file}' not found. Please check the file path.")