import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Oslo Mobility Analytics",
    layout="wide",
)

st.title("🚆 Oslo Mobility Analytics Dashboard")

gold_dir = Path("data")

st.markdown(
    """
    This dashboard will visualize mobility analytics
    generated from Entur public transport data.
    """
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Departures", "N/A")
col2.metric("Delay Rate", "N/A")
col3.metric("Average Delay", "N/A")

st.subheader("Line Performance")

sample_df = pd.DataFrame(
    {
        "line": ["L1", "RE11", "R21"],
        "delay_rate_pct": [40, 20, 5],
    }
)

st.bar_chart(
    sample_df.set_index("line")
)

st.success("Dashboard initialized successfully.")
