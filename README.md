# Aviation Data Pipeline

This project explores aviation data from the OpenSky API and incrementally builds a data pipeline for ingestion, transformation, and orchestration using Apache Airflow.

## Overview

The goals of this project are to:

- Retrieve aviation data from the <u>OpenSky API</u>  
- Explore and understand the dataset structure  
- Transform raw state vectors into a structured format  
- Establish the foundation for an ETL pipeline using <u>Apache Airflow</u>
- Clean, enrich, and model raw data to support additional analysis and business intelligence use cases
- Visualize aviation data and derived insights
- Automate the pipeline to build a reliable system that keeps recent data queryable for analytical purposes while archiving historical data for future retrieval

## Pipeline Architecture
OpenSky API → Airflow DAG → Transform (Pandas) → Validate (Pandera) → Parquet → PostgreSQL
(Currently being refactored after recognizing that constant file I/O between <u>Apache Airflow</u> tasks is unnecessary for preventing in-memory data persistence.)

## Current Status

### Pipeline Implementation
- Data extraction from <u>OpenSky API</u>  
- Transformation of state vectors into tabular format
- Loading from Parquet into local <u>PostgreSQL</u> database on on a separated VM within a private network
- Execution of the workflow using Apache Airflow Containers on host OS
- Extraction of raw data from raw_layer, cleansing and transformation of the dataset, and loading of processed data into the cleaned_layer

### Orchestration
- DAG scheduling has been implemented and verified (automatic scheduled runs working)  
- Pipeline logic has been modularized

### Engineering Improvements
- Basic schema definition has been introduced for transformed data columns  
- Added basic error detection for API requests and transformation steps; comprehensive error handling has not yet been implemented

### Data Validation

Introduced validations module: 
- Verify that raw payloads conform to expected structural and data type requirements
- Log valid and invalid records during processing raw data

### Design decisions
- Data is stored in `/tmp` inside the container (ephemeral storage)
- The initial decision to implement multiple file read/write operations during extraction and ingestion into the raw_layer was based on the misconception that ETL pipelines must always be separated into distinct Extract, Transform, and Load stages
- Configuration values and connection parameters have been externalized from the source code

### Limitations
- Data can be persistant accross container restarts, but has to be implemented by using the DB accordingly
- Basic error detection on some parts exists for read/write operations, but no full retry or recovery has been implemented strategy yet  
- Schema validation has been improved, but its integration remains limited due to earlier architectural misconceptions regarding ETL task separation
- Pipeline is still in early testing phase and primarily manually triggered for debugging
- The initial ingestion pipeline for API extraction still performs intermediate file read/write operations between tasks, resulting in unnecessary I/O overhead

### Next Improvements

#### Data Layer
- Design layered raw / cleaned /enriched / BI architecture within <u>PostgreSQL</u>
- Improve schema enforcement and validation during transformation stages
- Enrich data for future analysis
- Model data using dimensional modeling principles

#### Pipeline
- Build the initial data cleaning, enrichment, and modeling workflows using the database as the central storage architecture
- Establish fixed scheduling intervals for automated data ingestion and update cycles
- Use database as the acctual data storage instead of writing into ephemeral storage between tasks.
- Improve scheduling strategy (move beyond manual triggering)

#### Exploration
- Explore 24/7 extraction boundaries using authenticated API access
- Migrate <u>Apache Airflow</u> from the host OS to a dedicated server to enable continuous 24/7 orchestration
- Evaluate limits of infrastructure and consider adding worker containers for independant DAG execution
- Investigate object storage solutions for archival data, as well as audit logs and pipeline logging artifacts
- reason about the seperation of analytical BI values stored within RDBMS and and a seperate near real time presentation of geospatial positions of airplanes using grafana
- examine possibilities of messaging possibilities on different logging levels

#### Long-Term Vision
- Design separation between analytical BI datasets stored in a relational database and a near real-time geospatial visualization layer for aircraft positions using tools such as Grafana
- Explore messaging and event-driven architectures based on different logging levels for improved observability and system responsiveness

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
