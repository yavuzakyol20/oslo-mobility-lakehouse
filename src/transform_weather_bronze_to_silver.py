import json
from datetime import datetime, timezone

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"


def get_service_client():
    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()
    return DataLakeServiceClient(account_url=account_url, credential=credential)


def get_latest_bronze_weather_file(file_system_client):
    paths = file_system_client.get_paths(path="bronze/weather")

    json_files = [
        path.name for path in paths
        if path.name.endswith(".json")
    ]

    if not json_files:
        raise FileNotFoundError("No bronze weather JSON files found")

    return sorted(json_files)[-1]


def read_json_from_adls(file_system_client, path):
    file_client = file_system_client.get_file_client(path)
    data = file_client.download_file().readall()
    return json.loads(data.decode("utf-8"))


def upload_parquet_to_adls(file_system_client, df):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    remote_path = f"silver/weather/oslo_weather_clean_{timestamp}.parquet"

    parquet_bytes = df.to_parquet(index=False)

    file_client = file_system_client.get_file_client(remote_path)
    file_client.upload_data(parquet_bytes, overwrite=True)

    print(f"Uploaded silver parquet to {remote_path}")


def main():
    service_client = get_service_client()
    file_system_client = service_client.get_file_system_client(FILE_SYSTEM)

    bronze_path = get_latest_bronze_weather_file(file_system_client)
    raw = read_json_from_adls(file_system_client, bronze_path)

    current = raw["current"]

    df = pd.DataFrame([{
        "city": "Oslo",
        "latitude": raw.get("latitude"),
        "longitude": raw.get("longitude"),
        "timezone": raw.get("timezone"),
        "observation_time": current.get("time"),
        "temperature_2m": current.get("temperature_2m"),
        "wind_speed_10m": current.get("wind_speed_10m"),
        "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": bronze_path,
    }])

    upload_parquet_to_adls(file_system_client, df)


if __name__ == "__main__":
    main()
