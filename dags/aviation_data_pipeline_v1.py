import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG

from plugins.etl.extract import extract_from_api
from plugins.etl.transform import transform_raw_data
from plugins.etl.load import load_files

from pathlib import Path

from plugins.utils.file_io import read_parquet



start = pendulum.datetime(2026 , 4, 27 , 13, 59, tz="Europe/Berlin")
#end = start.add(minutes=60)



def _extract_data(ti):

    run_id = ti.run_id.replace(":", "_")

    extract_from_api(run_id=run_id)

    return run_id

def _transform_data(ti):

    run_id = ti.xcom_pull(task_ids="extract_data")

    transform_raw_data(run_id=run_id)

    return run_id

def _load_data(ti):

    run_id = ti.xcom_pull(task_ids="transform_data")

    load_files(run_id=run_id)

    return run_id

def _notify(ti):
    #note: for verification purpose, has to be removed
    run_id = ti.xcom_pull(task_ids="transform_data")

    raw_data = read_parquet(Path(f"/tmp/transformed/opensky_transformed_{run_id}.parquet"))

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



