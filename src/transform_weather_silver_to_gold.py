from datetime import datetime, timezone
from io import BytesIO

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"


def get_service_client():
    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()
    return DataLakeServiceClient(account_url=account_url, credential=credential)


def latest_silver_file(fs_client):
    files = [
        p.name
        for p in fs_client.get_paths(path="silver/weather")
        if p.name.endswith(".parquet")
    ]

    if not files:
        raise FileNotFoundError("No silver parquet found")

    return sorted(files)[-1]


def read_parquet(fs_client, path):
    file_client = fs_client.get_file_client(path)
    raw = file_client.download_file().readall()
    return pd.read_parquet(BytesIO(raw))


def upload_gold(fs_client, df):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    remote_path = (
        f"gold/weather/weather_summary_{timestamp}.parquet"
    )

    parquet_bytes = df.to_parquet(index=False)

    file_client = fs_client.get_file_client(remote_path)
    file_client.upload_data(parquet_bytes, overwrite=True)

    print(f"Uploaded gold summary to {remote_path}")


def main():
    service_client = get_service_client()
    fs_client = service_client.get_file_system_client(FILE_SYSTEM)

    silver_path = latest_silver_file(fs_client)
    df = read_parquet(fs_client, silver_path)

    summary = pd.DataFrame([
        {
            "city": "Oslo",
            "temperature_c": float(df["temperature_2m"].iloc[0]),
            "wind_speed_kmh": float(df["wind_speed_10m"].iloc[0]),
            "observation_time": df["observation_time"].iloc[0],
            "processed_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        }
    ])

    upload_gold(fs_client, summary)


if __name__ == "__main__":
    main()
