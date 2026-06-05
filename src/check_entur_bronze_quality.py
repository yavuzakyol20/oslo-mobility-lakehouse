import json

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"


def get_fs_client():
    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
    return service_client.get_file_system_client(FILE_SYSTEM)


def latest_bronze_file(fs_client):
    files = [
        p.name
        for p in fs_client.get_paths(path="bronze/entur/departures")
        if p.name.endswith(".json")
    ]

    if not files:
        raise FileNotFoundError("No Entur bronze files found")

    return sorted(files)[-1]


def main():
    fs_client = get_fs_client()
    path = latest_bronze_file(fs_client)

    raw = fs_client.get_file_client(path).download_file().readall()
    data = json.loads(raw.decode("utf-8"))

    stop_place = data["payload"]["data"]["stopPlace"]
    calls = stop_place["estimatedCalls"]

    if stop_place["name"] != "Oslo S":
        raise ValueError("Unexpected stop name")

    if len(calls) == 0:
        raise ValueError("No departures found")

    required_fields = [
        "aimedDepartureTime",
        "expectedDepartureTime",
        "destinationDisplay",
        "serviceJourney",
    ]

    for call in calls:
        for field in required_fields:
            if field not in call:
                raise ValueError(f"Missing field: {field}")

    print(f"Data quality passed for {path}")
    print(f"Departure count: {len(calls)}")


if __name__ == "__main__":
    main()
