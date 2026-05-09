# Aviation Data Pipeline

This project explores aviation data from the OpenSky API and incrementally builds a data pipeline for ingestion, transformation, and orchestration using Apache Airflow.

## Overview

The goals of this project are to:

- Retrieve aviation data from the OpenSky API  
- Explore and understand the dataset structure  
- Transform raw state vectors into a structured format  
- Establish the foundation for an ETL pipeline using Apache Airflow  

## Pipeline Architecture
OpenSky API → Airflow DAG → Transform (Pandas) → Validate (Pandera) → CSV → PostgreSQL

## Current Status

### Pipeline Implementation
- Data extraction from OpenSky API  
- Transformation of state vectors into tabular format
- Loading from CSV into local PostgreSQL DB on on a separated VM within a private network
- Execution of the workflow using Apache Airflow Containers on host OS

### Orchestration
- DAG scheduling has been implemented and verified (automatic scheduled runs working)  
- Pipeline logic has been partially modularized (configuration values like paths and API endpoints are now variable-based instead of fully hardcoded)  

### Engineering Improvements
- Basic schema definition has been introduced for transformed data columns  
- Initial error handling added for API requests and data transformation steps  


### Data Validation

Introduced validations module: `plugins/validations/schema.py` `plugins/validations/validate_schema.py`

- `aviation_schema`
- `validate_dataframe_schema(df, path)`

Updated Docker Compose .env to include:
`_PIP_ADDITIONAL_REQUIREMENTS=pandera`
`POSTGRES_USER`
`POSTGRES_PASSWORD`
`POSTGRES_HOST`
`POSTGRES_PORT`
`POSTGRES_DB`

This allows:
- schema validation via Pandera
- externalized database configuration (no hardcoding inside DAGs)


### Design decisions
- Data is stored in `/tmp` inside the container (ephemeral storage)
- Pipeline logic is implemented directly inside the DAG  
- Focus on simplicity to verify functionality before adding complexity  
- Some configuration values (paths, API endpoints) have been extracted into variables

### Limitations
- Data is not persisted across container restarts 
- Basic error handling exists for read/write operations, but no full retry strategy yet  
- Schema validation is still minimal (initial Pandera integration only)
- Some configuration values are still partially hardcoded
- Pipeline is still in early testing phase and primarily manually triggered for debugging

### Next Improvements

#### Data Layer
- Design staging structure inside PostgreSQL
- Improve schema enforcement during transformation
- Transform data into more structured relational format

#### Pipeline
- Strengthen schema validation using Pandera
- Add backfilling support from API
- Improve scheduling strategy (move beyond manual triggering)

#### Exploration
- Adjust scope of fetched data (e.g. filter by country)
- Explore 24/7 ingestion possibilities with authenticated API access


## Project Structure

- `notebooks/` – exploratory analysis and experimentation
- `config/` – Central configuration files (API settings, paths, schema definitions)
- `plugins/` – Reusable utility modules (e.g. file I/O helpers for DAGs)
- `dags/` – Airflow DAG definitions for orchestration
- `data/` – raw and processed datasets (excluded from version control)  


> Note: The Airflow infrastructure is not part of this project. It is used as an external development environment for learning and pipeline testing.

This serves as the initial proof of concept for integrating ingestion, transformation, and orchestration.

## Tech Stack

- Python  
- Pandas  
- OpenSky API  
- Apache Airflow

## Status

🚧 Work in progress
