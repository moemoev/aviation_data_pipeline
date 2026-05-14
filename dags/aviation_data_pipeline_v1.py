import pandas as pd
import yaml
import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from airflow.operators.python import get_current_context

import os
from sqlalchemy import create_engine

from plugins.etl.transform import transform_raw_data
from plugins.etl.extract import extract_from_api

from plugins.utils.file_io import read_parquet





with open("config/path_config.yaml", "r") as file:
    path = yaml.safe_load(file)

with open("config/schema_config.yaml", "r") as file:
    schema = yaml.safe_load(file)


PATH_RAW = path['paths']['raw_storage']
PATH_TRANSFORMED = path['paths']['transformed_storage']
PATH_CUSTOM_LOGS = path['paths']['logs_storage']

CONN_POSTGRESQL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}")

start = pendulum.datetime(2026 , 4, 27 , 13, 59, tz="Europe/Berlin")
#end = start.add(minutes=60)



def _extract_data(ti):

    run_id = ti.run_id.replace(":", "_")

    extract_from_api(run_id=run_id, path=PATH_RAW)

    return run_id

def _transform_data(ti):

    run_id = ti.xcom_pull(task_ids="extract_data")

    transform_raw_data(
        run_id=run_id,
        path_raw=PATH_RAW,
        path_transformed=PATH_TRANSFORMED,
        path_custom_logs=PATH_CUSTOM_LOGS
    )

    return run_id

def _load_data(ti):

    run_id = ti.xcom_pull(task_ids="transform_data")

    file_path = f"{PATH_TRANSFORMED}/opensky_transformed_{run_id}.parquet"

    df = pd.read_parquet(file_path)

    engine = create_engine(CONN_POSTGRESQL)

    df.to_sql("data", con=engine, index=False, if_exists="replace")

    return run_id

def _notify(ti):
    run_id = ti.xcom_pull(task_ids="transform_data")

    file_path = f"{PATH_TRANSFORMED}/opensky_transformed_{run_id}.parquet"

    raw_data = read_parquet(file_path)

    total_rows = raw_data.shape[0]
    timestamp = raw_data["time"].unique()

    print(f"Parquet Summary:")
    print(f"- Rows: {total_rows}")
    print(f"- time: {timestamp}")

    return

with DAG(
    dag_id="aviation_data_pipeline_v1",
    start_date=start,
    #end_date=end,
    schedule=None, #"*/5 * * * *",
    catchup=False,
):
    extract_data = PythonOperator(task_id="extract_data", python_callable=_extract_data)

    transform_data = PythonOperator(task_id="transform_data", python_callable=_transform_data)

    load_data = PythonOperator(task_id="load_data", python_callable=_load_data)

    notify = PythonOperator(task_id="notify", python_callable=_notify)

    extract_data >> transform_data >> load_data >> notify



