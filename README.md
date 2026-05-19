# Oslo Mobility Lakehouse

End-to-end data engineering project using Python, pandas and Lakehouse architecture principles.

## Project Architecture

```text
Bronze Layer  -> Raw weather data
Silver Layer  -> Cleaned and standardized data
Gold Layer    -> Aggregated analytics data

## Data Engineering Concepts Covered

- Data ingestion from external APIs
- Bronze/Silver/Gold Lakehouse architecture
- Data quality validation
- PySpark-based transformations
- Airflow DAG orchestration
- Docker containerization
- GitHub Actions CI/CD
- Infrastructure as Code with Terraform
- Databricks-style notebook workspace
