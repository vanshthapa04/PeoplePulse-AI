import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="PeoplePulse AI",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path(__file__).parent / "assets" / "style.css"

if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("👥 PeoplePulse AI")

st.subheader("Employee Attrition Analytics Platform")

st.markdown("---")

st.markdown("""
Welcome to **PeoplePulse AI**.

Use the navigation sidebar to explore:

- 📊 Dashboard
- 👥 Employee Explorer
- 🤖 Attrition Prediction
- 🚨 High Risk Employees
- 📈 SQL Insights
""")

st.info("Select a page from the sidebar to begin.")