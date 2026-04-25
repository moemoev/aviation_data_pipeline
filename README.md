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

## Project Structure

- `notebooks/` – exploratory analysis and experimentation  
- `src/` – reusable pipeline components (in progress)  
- `airflow/` – DAG definitions for orchestration (planned)  
- `data/` – raw and processed datasets (excluded from version control)  

## Next Steps

The next phase focuses on introducing Apache Airflow for pipeline orchestration.

A pre-existing Airflow setup from *Data Engineering with Apache Airflow* is used as a **local development environment**. This provides Docker configuration and base Airflow services required to run and test DAGs.

> Note: The Airflow infrastructure is not part of this project. It is used as an external development environment for learning and pipeline testing.

The first DAG will:

- Fetch aviation data from the OpenSky API  
- Apply the existing transformation logic  
- Store the processed dataset locally as a CSV file  

This will serve as a proof of concept for integrating ingestion, transformation, and orchestration.

## Tech Stack

- Python  
- Pandas  
- OpenSky API  
- Apache Airflow (in progress)  

## Status

🚧 Work in progress
