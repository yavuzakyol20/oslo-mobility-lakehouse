import pandas as pd
import streamlit as st
from io import BytesIO

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"
GOLD_PATH = "gold/entur/line_performance"


st.set_page_config(
    page_title="Oslo Mobility Analytics",
    layout="wide",
)

st.title("🚆 Oslo Mobility Analytics Dashboard")
st.markdown("Realtime public transport analytics from Entur data stored in Azure Data Lakehouse.")


@st.cache_data
def load_latest_line_performance():
    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(
        account_url=account_url,
        credential=credential,
    )

    fs_client = service_client.get_file_system_client(FILE_SYSTEM)

    parquet_files = [
        p.name
        for p in fs_client.get_paths(path=GOLD_PATH)
        if p.name.endswith(".parquet")
    ]

    if not parquet_files:
        return pd.DataFrame()

    latest_file = sorted(parquet_files)[-1]

    raw = fs_client.get_file_client(latest_file).download_file().readall()
    df = pd.read_parquet(BytesIO(raw))

    return df


df = load_latest_line_performance()

if df.empty:
    st.warning("No Gold line performance data found.")
    st.stop()

total_departures = int(df["total_departures"].sum())
delayed_departures = int(df["delayed_departures"].sum())
delay_rate = round(delayed_departures / total_departures * 100, 2)
avg_delay = round(df["avg_delay_minutes"].mean(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Departures", total_departures)
col2.metric("Delay Rate", f"{delay_rate}%")
col3.metric("Average Delay", f"{avg_delay} min")

st.subheader("Delay Rate by Line")

chart_df = df[["line_code", "delay_rate_pct"]].set_index("line_code")
st.bar_chart(chart_df)

st.subheader("Line Performance Data")
st.dataframe(df, use_container_width=True)

st.success("Dashboard loaded from Azure Gold layer.")
