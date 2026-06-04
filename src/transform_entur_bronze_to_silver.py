import json
from datetime import datetime, timezone
from io import BytesIO

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"


def get_file_system_client():
    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(
        account_url=account_url,
        credential=credential,
    )
    return service_client.get_file_system_client(FILE_SYSTEM)


def latest_bronze_entur_file(fs_client):
    files = [
        p.name
        for p in fs_client.get_paths(path="bronze/entur/departures")
        if p.name.endswith(".json")
    ]

    if not files:
        raise FileNotFoundError("No Entur bronze JSON files found")

    return sorted(files)[-1]


def read_json(fs_client, path):
    file_client = fs_client.get_file_client(path)
    raw = file_client.download_file().readall()
    return json.loads(raw.decode("utf-8"))


def normalize_departures(raw):
    stop = raw["payload"]["data"]["stopPlace"]
    rows = []

    for call in stop["estimatedCalls"]:
        line = call["serviceJourney"]["line"]

        rows.append({
            "stop_id": stop["id"],
            "stop_name": stop["name"],
            "line_code": line["publicCode"],
            "line_name": line["name"],
            "transport_mode": line["transportMode"],
            "destination": call["destinationDisplay"]["frontText"],
            "aimed_departure_time": call["aimedDepartureTime"],
            "expected_departure_time": call["expectedDepartureTime"],
            "realtime": call["realtime"],
            "source_file": raw.get("source"),
            "bronze_file": raw.get("stop_id"),
            "processed_at_utc": datetime.now(timezone.utc).isoformat(),
        })

    return pd.DataFrame(rows)


def upload_silver(fs_client, df):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    remote_path = (
        f"silver/entur/departures/"
        f"oslo_s_departures_clean_{timestamp}.parquet"
    )

    parquet_bytes = df.to_parquet(index=False)

    file_client = fs_client.get_file_client(remote_path)
    file_client.upload_data(parquet_bytes, overwrite=True)

    print(f"Uploaded Entur silver parquet to {remote_path}")


def main():
    fs_client = get_file_system_client()
    bronze_path = latest_bronze_entur_file(fs_client)
    raw = read_json(fs_client, bronze_path)

    df = normalize_departures(raw)
    upload_silver(fs_client, df)


if __name__ == "__main__":
    main()
