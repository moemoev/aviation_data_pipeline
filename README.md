# Aviation Data Pipeline

This project explores aviation data from the OpenSky API and incrementally builds a data pipeline for ingestion, transformation, and orchestration using Apache Airflow.

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
- Execution of the workflow using Apache Airflow

- DAG scheduling has been implemented and verified (automatic scheduled runs working)  
- Pipeline logic has been partially modularized (configuration values like paths and API endpoints are now variable-based instead of fully hardcoded)  
- Basic schema definition has been introduced for transformed data columns  
- Initial error handling added for API requests and data transformation steps  

## Version 1 – Minimal Working Pipeline

This version implements a minimal end-to-end data pipeline using Apache Airflow.

### What it does
- Fetches aviation data from the OpenSky API  
- Transforms the raw JSON response into a structured tabular format  
- Stores the processed data as a CSV file inside the Airflow worker container  
- Executes the workflow through an Airflow DAG  

### Utility Refactor (Recent Update)

Introduced reusable utility module: `plugins/utils/file_io.py`

- `read_json(path)`
- `read_csv(path)`

Added `__init__.py` files to enable proper Python package imports:
`plugins/__init__.py`, `plugins/utils/__init__.py`

Updated Docker Compose to include:

`PYTHONPATH=/opt/airflow/plugins`

This allows DAGs to import custom utility functions.

### Purpose
The goal of this version is to validate the core pipeline flow:
ingestion → transformation → storage → orchestration.

### Design decisions
- Data is stored in `/tmp` inside the container (ephemeral storage)  
- Pipeline logic is implemented directly inside the DAG  
- Focus on simplicity to verify functionality before adding complexity  
- Some configuration values (paths, API endpoints) have been extracted into variables to reduce hardcoding  

### Limitations
- Data is not persisted across container restarts  
- Basic error handling exists, but no full retry strategy yet  
- Schema validation is only partially implemented via configuration definitions  
- Some file paths and configuration values are still hardcoded in parts of the pipeline  
- Pipeline is now scheduled, but still in early testing phase

### Next Improvements
- Improve error handling and logging consistency across all tasks  
- Fully refactor remaining hardcoded values into configuration layer  
- Strengthen schema validation and enforce it during transformation 
- Refactor logic into reusable modules (`src/`)  
- Replace CSV with a more robust storage solution (e.g. Parquet or database) 

## Project Structure

- `notebooks/` – exploratory analysis and experimentation
- `config/` – Central configuration files (API settings, paths, schema definitions)
- `plugins/` – Reusable utility modules (e.g. file I/O helpers for DAGs)
- `dags/` – Airflow DAG definitions for orchestration
- `data/` – raw and processed datasets (excluded from version control)  

## Next Steps

The next phase focuses on improving and extending the existing Airflow pipeline.

The project uses a local Airflow Docker environment (based on a pre-configured setup) for orchestration and testing. This environment is external to the project and used only for development purposes.

> Note: The Airflow infrastructure is not part of this project. It is used as an external development environment for learning and pipeline testing.

The first DAG:

- Fetches aviation data from the OpenSky API  
- Applies the transformation logic  
- Stores the processed dataset locally as a CSV file  
- Runs on a scheduled interval using Airflow (automated execution enabled)
- 
This serves as the initial proof of concept for integrating ingestion, transformation, and orchestration.

## Tech Stack

- Python  
- Pandas  
- OpenSky API  
- Apache Airflow

## Status

🚧 Work in progress
