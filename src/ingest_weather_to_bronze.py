import json
from datetime import datetime, timezone

import requests
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"

LAT = 59.9139
LON = 10.7522


def fetch_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,wind_speed_10m"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def upload_json(data):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    remote_path = f"bronze/weather/oslo_weather_{timestamp}.json"

    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(
        account_url=account_url,
        credential=credential,
    )

    file_system_client = service_client.get_file_system_client(FILE_SYSTEM)
    file_client = file_system_client.get_file_client(remote_path)

    payload = json.dumps(data, indent=2).encode("utf-8")
    file_client.upload_data(payload, overwrite=True)

    print(f"Uploaded weather data to {remote_path}")


def main():
    data = fetch_weather()
    upload_json(data)


if __name__ == "__main__":
    main()
