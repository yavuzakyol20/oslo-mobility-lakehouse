
from azure.identity import DefaultAzureCredential

from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_NAME = "oslomobilitylakehouse"

FILE_SYSTEM = "lakehouse"

LOCAL_FILE = "test_upload.txt"

REMOTE_PATH = "bronze/test_upload_python.txt"

def main():

    account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"

    credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(

        account_url=account_url,

        credential=credential,

    )

    file_system_client = service_client.get_file_system_client(FILE_SYSTEM)

    file_client = file_system_client.get_file_client(REMOTE_PATH)

    with open(LOCAL_FILE, "rb") as file:

        file_client.upload_data(file, overwrite=True)

    print(f"Uploaded {LOCAL_FILE} to {REMOTE_PATH}")

if __name__ == "__main__":

    main()

