# Local Airflow Orchestration

This folder contains the Airflow DAG used to orchestrate the weather Lakehouse pipeline.

## Run Airflow locally

Start Airflow with Docker Compose:

```bash
docker compose -f docker-compose.airflow.yml up
