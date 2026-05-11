import pandas as pd
import yaml
import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from airflow.operators.python import get_current_context

import os
from sqlalchemy import create_engine

from plugins.validations.validate_schema import validate_dataframe_schema
from plugins.etl.transform import transform_raw_data
from plugins.utils.api_io import request_api
from plugins.utils.file_io import read_json, read_csv, write_json, write_csv
from plugins.utils.generate_token import get_token




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
# end = start.add(minutes=2)



def _extract_data(ti):

    token = get_token()

    run_id = ti.run_id.replace(":", "_")
    data = request_api(token=token)

    # write data to file
    write_json(path=PATH_RAW, file_name=f"opensky_raw_{run_id}", data=data)

    return run_id

def _transform_data(ti):

    run_id = ti.xcom_pull(task_ids="extract_data")

    source_file_path = f"{PATH_RAW}/opensky_raw_{run_id}.json"

    raw_data = read_json(source_file_path)

    transformed_data = transform_raw_data(raw_data)

    validate_dataframe_schema(transformed_data, path=PATH_CUSTOM_LOGS)

    write_csv(path=PATH_TRANSFORMED, file_name=f"opensky_transformed_{run_id}", data=transformed_data)


    return run_id

def _load_data(ti):

    run_id = ti.xcom_pull(task_ids="transform_data")

    file_path = f"{PATH_TRANSFORMED}/opensky_transformed_{run_id}.csv"

    df = pd.read_csv(file_path)

    engine = create_engine(CONN_POSTGRESQL)

    df.to_sql("data", con=engine, index=False, if_exists="replace")

    return run_id

def notify(ti):
    run_id = ti.xcom_pull(task_ids="transform_data")

    file_path = f"{PATH_TRANSFORMED}/opensky_transformed_{run_id}.csv"

    raw_data = read_csv(file_path)

    total_rows = raw_data.shape[0]
    timestamp = raw_data["time"].unique()

    print(f"CSV Summary:")
    print(f"- Rows: {total_rows}")
    print(f"- time: {timestamp}")

    return

with DAG(
    dag_id="aviation_data_pipeline_v1",
    start_date=start,
    # end_date=end,
    schedule=None,
    catchup=False,
):
    extract_data = PythonOperator(task_id="extract_data", python_callable=_extract_data)

    transform_data = PythonOperator(task_id="transform_data", python_callable=_transform_data)

    load_data = PythonOperator(task_id="load_data", python_callable=_load_data)

    notify = PythonOperator(task_id="notify", python_callable=notify)

    extract_data >> transform_data >> load_data >> notify



