![CI](https://github.com/yavuzakyol20/oslo-mobility-lakehouse/actions/workflows/ci.yml/badge.svg)

Oslo Mobility Lakehouse

An end-to-end Azure-based Lakehouse platform that ingests, transforms, analyzes and visualizes real-time public transportation data from Entur (Norwegian public transport data platform).

Overview

This project demonstrates modern Data Engineering, Cloud and DevOps practices by implementing a complete Lakehouse architecture on Microsoft Azure.

The platform automatically ingests real-time transport departure data, validates data quality, transforms datasets through Bronze/Silver/Gold layers, orchestrates workflows with Airflow, manages infrastructure using Terraform, and presents analytics through an interactive Streamlit dashboard.

⸻

Architecture

Entur API
    │
    ▼
Bronze Layer (Raw JSON)
    │
    ▼
Silver Layer (Partitioned Parquet)
    │
    ▼
Gold Layer (Analytics Datasets)
    │
    ▼
Streamlit Dashboard

Infrastructure

Azure Data Lake Storage Gen2
        │
Terraform (IaC)
        │
GitHub Actions CI/CD
        │
Apache Airflow

⸻

Features

Data Ingestion

* Real-time public transport departure data from Entur API
* Automated ingestion to Azure Data Lake Storage Gen2
* Bronze layer storage in JSON format

Data Quality

* Automated validation of incoming datasets
* Record count checks
* Data completeness verification

Data Transformation

* Bronze → Silver normalization
* Delay calculation and enrichment
* Partitioned storage design
* Historical dataset accumulation

Analytics

Gold datasets include:

* Departure Summary
* Line Performance Analytics
* Delay Trend Analytics

Orchestration

* Apache Airflow DAGs
* Automated pipeline execution
* Workflow dependency management

Infrastructure as Code

* Azure Resource Group managed with Terraform
* Azure Storage Account managed with Terraform
* Declarative infrastructure provisioning

CI/CD

GitHub Actions pipeline includes:

* Python validation
* Terraform validation
* Docker build verification

Dashboard

Interactive Streamlit dashboard featuring:

* Total Departures
* Delay Rate
* Average Delay
* Top Delayed Lines
* Historical Delay Trends

⸻

Technologies

Cloud & Infrastructure

* Microsoft Azure
* Azure Data Lake Storage Gen2
* Terraform
* Docker

Data Engineering

* Python
* Pandas
* PyArrow
* Apache Airflow

DevOps

* GitHub Actions
* CI/CD
* Infrastructure as Code (IaC)

Visualization

* Streamlit

⸻

Skills Demonstrated

* Data Engineering
* Cloud Engineering
* Platform Engineering
* Infrastructure as Code (Terraform)
* CI/CD Pipelines
* Azure Cloud Services
* Data Lakehouse Architecture
* Workflow Orchestration
* Data Quality Engineering
* Dashboard Development

⸻

Future Improvements

* Azure Kubernetes Service (AKS)
* GitOps deployment workflows
* Managed Identity authentication
* Automated infrastructure deployment
* Power BI integration
* Real-time streaming analytics
