from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_PATH = "/opt/airflow/project"
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_PATH = "/opt/airflow/project"

with DAG(
    dag_id="weather_lakehouse_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    description="Azure Lakehouse Weather Pipeline",
) as dag:

    ingest_weather = BashOperator(
        task_id="ingest_weather",
        bash_command=f"cd {PROJECT_PATH} && python src/ingest_weather_to_bronze.py",
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command=f"cd {PROJECT_PATH} && python src/transform_weather_bronze_to_silver.py",
    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command=f"cd {PROJECT_PATH} && python src/transform_weather_silver_to_gold.py",
    )

    ingest_weather >> bronze_to_silver >> silver_to_gold
