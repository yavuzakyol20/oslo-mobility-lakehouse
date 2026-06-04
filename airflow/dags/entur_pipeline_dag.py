from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_PATH = "/opt/airflow/project"

with DAG(
    dag_id="entur_lakehouse_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
    description="Entur Oslo Mobility Lakehouse Pipeline",
) as dag:

    ingest_entur = BashOperator(
        task_id="ingest_entur_departures",
        bash_command=f"cd {PROJECT_PATH} && python src/ingest_entur_departures_to_bronze.py",
    )

    bronze_to_silver = BashOperator(
        task_id="entur_bronze_to_silver",
        bash_command=f"cd {PROJECT_PATH} && python src/transform_entur_bronze_to_silver.py",
    )

    silver_to_gold = BashOperator(
        task_id="entur_silver_to_gold",
        bash_command=f"cd {PROJECT_PATH} && python src/transform_entur_silver_to_gold.py",
    )

    ingest_entur >> bronze_to_silver >> silver_to_gold
