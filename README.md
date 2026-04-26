# Aviation Data Pipeline

This project explores aviation data from the OpenSky API and incrementally builds a data pipeline for ingestion, transformation, and orchestration.

## Overview

The goals of this project are to:

- Retrieve aviation data from the OpenSky API  
- Explore and understand the dataset structure  
- Transform raw state vectors into a structured format  
- Establish the foundation for an ETL pipeline using Apache Airflow  

## Current Status

- Data extraction from OpenSky API  
- Initial data exploration using Jupyter notebooks  
- Transformation of state vectors into tabular format  

## Version 1 – Minimal Working Pipeline

This version implements a minimal end-to-end data pipeline using Apache Airflow.

### What it does
- Fetches aviation data from the OpenSky API  
- Transforms the raw JSON response into a structured tabular format  
- Stores the processed data as a CSV file inside the Airflow worker container  
- Executes the workflow through an Airflow DAG  

### Purpose
The goal of this version is to validate the core pipeline flow:
ingestion → transformation → storage → orchestration.

### Design decisions
- Data is stored in `/tmp` inside the container (ephemeral storage)  
- Pipeline logic is implemented directly inside the DAG  
- Focus on simplicity to verify functionality before adding complexity  

### Limitations
- Data is not persisted across container restarts  
- No error handling or retry logic  
- No schema validation or type enforcement  
- Hardcoded file paths and API endpoint  
- Pipeline is triggered manually (no scheduling yet)  

### Next Improvements
- Add error handling and logging  
- Introduce scheduling in Airflow  
- Refactor logic into reusable modules (`src/`)  
- Add data validation and schema checks  
- Replace CSV with a more robust storage solution (e.g. Parquet or database) 

## Project Structure

- `notebooks/` – exploratory analysis and experimentation  
- `src/` – reusable pipeline components (in progress)  
- `dags/` – Airflow DAG definitions for orchestration
- `data/` – raw and processed datasets (excluded from version control)  

## Next Steps

The next phase focuses on improving and extending the existing Airflow pipeline.

A pre-existing Airflow setup from *Data Engineering with Apache Airflow* is used as a **local development environment**. This provides Docker configuration and base Airflow services required to run and test DAGs.

> Note: The Airflow infrastructure is not part of this project. It is used as an external development environment for learning and pipeline testing.

The first DAG:

- Fetches aviation data from the OpenSky API  
- Applies the transformation logic  
- Stores the processed dataset locally as a CSV file  

This serves as the initial proof of concept for integrating ingestion, transformation, and orchestration.

## Tech Stack

- Python  
- Pandas  
- OpenSky API  
- Apache Airflow

## Status

🚧 Work in progress
