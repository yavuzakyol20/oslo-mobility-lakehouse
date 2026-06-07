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
    service_client = DataLakeServiceClient(
        account_url=account_url,
        credential=credential,
    )
    return service_client.get_file_system_client(FILE_SYSTEM)


def load_all_silver_departures(fs_client):
    parquet_files = [
        p.name
        for p in fs_client.get_paths(path="silver/entur/departures")
        if p.name.endswith(".parquet")
    ]

    if not parquet_files:
        raise FileNotFoundError("No silver departure files found")

    dfs = []

    for path in parquet_files:
        raw = (
            fs_client.get_file_client(path)
            .download_file()
            .readall()
        )

        dfs.append(
            pd.read_parquet(BytesIO(raw))
        )

    return pd.concat(dfs, ignore_index=True)


def build_trends(df):
    trends = (
        df.groupby(
            ["departure_date", "transport_mode"]
        )
        .agg(
            total_departures=("line_code", "count"),
            delayed_departures=("is_delayed", "sum"),
            avg_delay_minutes=("delay_minutes", "mean"),
        )
        .reset_index()
    )

    trends["delay_rate_pct"] = (
        trends["delayed_departures"]
        / trends["total_departures"]
        * 100
    ).round(2)

    trends["processed_at_utc"] = (
        datetime.now(timezone.utc).isoformat()
    )

    return trends


def upload_gold(fs_client, df):
    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    remote_path = (
        "gold/entur/delay_trends/"
        f"delay_trends_{timestamp}.parquet"
    )

    parquet_bytes = df.to_parquet(index=False)

    fs_client.get_file_client(
        remote_path
    ).upload_data(
        parquet_bytes,
        overwrite=True,
    )

    print(
        f"Uploaded delay trends to {remote_path}"
    )


def main():
    fs_client = get_fs_client()

    df = load_all_silver_departures(fs_client)

    trends = build_trends(df)

    upload_gold(fs_client, trends)


if __name__ == "__main__":
    main()
