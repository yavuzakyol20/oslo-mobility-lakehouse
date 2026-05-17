from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_PATH = "/opt/airflow/oslo-mobility-lakehouse"

with DAG(
    dag_id="weather_lakehouse_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Orchestrates weather ingestion and transformation pipeline",
) as dag:

    ingest_weather = BashOperator(
        task_id="ingest_weather",
        bash_command=f"cd {PROJECT_PATH} && python src/ingestion/real_weather_ingestion.py",
    )

    data_quality_checks = BashOperator(
        task_id="data_quality_checks",
        bash_command=f"cd {PROJECT_PATH} && python src/utils/data_quality_checks.py",
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command=f"cd {PROJECT_PATH} && python src/transformations/bronze_to_silver_weather.py",
    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command=f"cd {PROJECT_PATH} && python src/transformations/silver_to_gold_weather.py",
    )

    ingest_weather >> data_quality_checks >> bronze_to_silver >> silver_to_gold
