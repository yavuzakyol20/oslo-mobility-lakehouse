from datetime import datetime, timezone
from io import BytesIO

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"


def get_fs_client():
    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
    return service_client.get_file_system_client(FILE_SYSTEM)


def latest_silver_file(fs_client):
    files = [
        p.name
        for p in fs_client.get_paths(path="silver/entur/departures")
        if p.name.endswith(".parquet")
    ]

    if not files:
        raise FileNotFoundError("No Entur silver parquet files found")

    return sorted(files)[-1]


def read_parquet(fs_client, path):
    file_client = fs_client.get_file_client(path)
    raw = file_client.download_file().readall()
    return pd.read_parquet(BytesIO(raw))


def build_gold_summary(df):
    df["aimed_departure_time"] = pd.to_datetime(df["aimed_departure_time"])
    df["expected_departure_time"] = pd.to_datetime(df["expected_departure_time"])

    df["delay_minutes"] = (
        df["expected_departure_time"] - df["aimed_departure_time"]
    ).dt.total_seconds() / 60

    summary = (
        df.groupby(["stop_name", "transport_mode"])
        .agg(
            departure_count=("line_code", "count"),
            delayed_departures=("delay_minutes", lambda x: (x > 0).sum()),
            avg_delay_minutes=("delay_minutes", "mean"),
            max_delay_minutes=("delay_minutes", "max"),
        )
        .reset_index()
    )

    summary["processed_at_utc"] = datetime.now(timezone.utc).isoformat()
    return summary


def upload_gold(fs_client, df):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    remote_path = f"gold/entur/departures/oslo_s_departure_summary_{timestamp}.parquet"

    parquet_bytes = df.to_parquet(index=False)

    file_client = fs_client.get_file_client(remote_path)
    file_client.upload_data(parquet_bytes, overwrite=True)

    print(f"Uploaded Entur gold summary to {remote_path}")


def main():
    fs_client = get_fs_client()
    silver_path = latest_silver_file(fs_client)
    df = read_parquet(fs_client, silver_path)

    gold_df = build_gold_summary(df)
    upload_gold(fs_client, gold_df)


if __name__ == "__main__":
    main()
