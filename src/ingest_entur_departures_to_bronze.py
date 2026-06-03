import json
from datetime import datetime, timezone

import requests
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"
FILE_SYSTEM = "lakehouse"

STOP_ID = "NSR:StopPlace:59872"  # Oslo S
STOP_NAME = "Oslo S"
ENTUR_URL = "https://api.entur.io/journey-planner/v3/graphql"


def fetch_departures():
    query = """
    query ($stopId: String!) {
      stopPlace(id: $stopId) {
        id
        name
        estimatedCalls(numberOfDepartures: 10) {
          realtime
          aimedDepartureTime
          expectedDepartureTime
          destinationDisplay {
            frontText
          }
          serviceJourney {
            line {
              publicCode
              name
              transportMode
            }
          }
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "ET-Client-Name": "yavuzakyol-oslo-mobility-lakehouse",
    }

    payload = {
        "query": query,
        "variables": {
            "stopId": STOP_ID,
        },
    }

    response = requests.post(
        ENTUR_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def upload_to_bronze(data):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    remote_path = (
        f"bronze/entur/departures/"
        f"oslo_s_departures_{timestamp}.json"
    )

    enriched_data = {
        "source": "entur_journey_planner_v3",
        "stop_id": STOP_ID,
        "stop_name": STOP_NAME,
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "payload": data,
    }

    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(
        account_url=account_url,
        credential=credential,
    )

    file_system_client = service_client.get_file_system_client(FILE_SYSTEM)
    file_client = file_system_client.get_file_client(remote_path)

    payload_bytes = json.dumps(
        enriched_data,
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")

    file_client.upload_data(payload_bytes, overwrite=True)

    print(f"Uploaded Entur departures to {remote_path}")


def main():
    data = fetch_departures()
    upload_to_bronze(data)


if __name__ == "__main__":
    main()
