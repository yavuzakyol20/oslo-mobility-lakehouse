# Oslo Mobility Lakehouse

![CI](https://github.com/yavuzakyol20/oslo-mobility-lakehouse/actions/workflows/ci.yml/badge.svg)


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

## Architecture

```text
External Weather API
        ↓
Bronze Layer (Parquet)
        ↓
Silver Layer (Cleaned Parquet)
        ↓
Gold Layer (Analytics Parquet)

## Azure Lakehouse Architecture

Pipeline flow:

API → Bronze → Silver → Gold

### Bronze
- Raw JSON weather data stored in Azure Data Lake Storage Gen2

### Silver
- Cleaned and standardized Parquet datasets

### Gold
- Analytics-ready weather summary datasets

### Technologies
- Python
- Azure Data Lake Storage Gen2
- Azure Identity
- Pandas
- PyArrow
- Apache Airflow
- Docker

