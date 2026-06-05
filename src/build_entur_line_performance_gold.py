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


def build_line_performance(df):
    summary = (
        df.groupby(["line_code", "line_name", "transport_mode"])
        .agg(
            total_departures=("line_code", "count"),
            delayed_departures=("is_delayed", "sum"),
            avg_delay_minutes=("delay_minutes", "mean"),
            max_delay_minutes=("delay_minutes", "max"),
        )
        .reset_index()
    )

    summary["on_time_departures"] = (
        summary["total_departures"] - summary["delayed_departures"]
    )

    summary["delay_rate_pct"] = (
        summary["delayed_departures"]
        / summary["total_departures"]
        * 100
    ).round(2)

    summary["avg_delay_minutes"] = summary["avg_delay_minutes"].round(2)
    summary["max_delay_minutes"] = summary["max_delay_minutes"].round(2)
    summary["processed_at_utc"] = datetime.now(timezone.utc).isoformat()

    return summary.sort_values(
        by=["delay_rate_pct", "avg_delay_minutes"],
        ascending=False,
    )


def upload_gold(fs_client, df):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    remote_path = (
        f"gold/entur/line_performance/"
        f"oslo_s_line_performance_{timestamp}.parquet"
    )

    parquet_bytes = df.to_parquet(index=False)

    file_client = fs_client.get_file_client(remote_path)
    file_client.upload_data(parquet_bytes, overwrite=True)

    print(f"Uploaded Entur line performance gold to {remote_path}")


def main():
    fs_client = get_fs_client()
    silver_path = latest_silver_file(fs_client)
    df = read_parquet(fs_client, silver_path)

    line_performance = build_line_performance(df)
    upload_gold(fs_client, line_performance)


if __name__ == "__main__":
    main()
