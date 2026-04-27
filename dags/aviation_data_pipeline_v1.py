import pandas as pd
import pathlib
import json
import yaml
import pendulum
import requests

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from airflow.operators.python import get_current_context


from plugins.utils.file_io import read_json, read_csv

with open("config/api_config.yaml", "r") as file:
    config = yaml.safe_load(file)

with open("config/path_config.yaml", "r") as file:
    path = yaml.safe_load(file)

with open("config/schema_config.yaml", "r") as file:
    schema = yaml.safe_load(file)

PATH_RAW = path['paths']['raw_storage']
PATH_TRANSFORMED = path['paths']['transformed_storage']

start = pendulum.datetime(2026 , 4, 27 , 13, 59, tz="Europe/Berlin")
end = start.add(minutes=2)



def _extract_data(ti):
    run_id = ti.run_id.replace(":", "_")

    pathlib.Path(PATH_RAW).mkdir(parents=True, exist_ok=True)

    url = config['aviation_api']
    response = requests.get(url)
    data = response.json()

    with open(f"{PATH_RAW}/opensky_raw_{run_id}.json", "w") as f:
        json.dump(data, f)

    return run_id

def _transform_data(ti):

    run_id = ti.xcom_pull(task_ids="extract_data")

    pathlib.Path(f"{PATH_TRANSFORMED}").mkdir(parents=True, exist_ok=True)

    columns = schema["aviation_states"]["columns"]

    file_path = f"{PATH_RAW}/opensky_raw_{run_id}.json"
    raw_data = read_json(file_path)

    transformed_data = pd.DataFrame(raw_data['states'])
    transformed_data.columns = columns[:transformed_data.shape[1]]
    transformed_data.insert(0, 'time', raw_data['time'])

    transformed_data.to_csv(f"{PATH_TRANSFORMED}/opensky_cleaned_{run_id}.csv", index=False)

    return run_id

def notify(ti):
    run_id = ti.xcom_pull(task_ids="transform_data")

    file_path = f"{PATH_TRANSFORMED}/opensky_cleaned_{run_id}.csv"

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
    end_date=end,
    schedule="* * * * *",
    catchup=False,
):
    extract_data = PythonOperator(task_id="extract_data", python_callable=_extract_data)

    transform_data = PythonOperator(task_id="transform_data", python_callable=_transform_data)

    notify = PythonOperator(task_id="notify", python_callable=notify)

    extract_data >> transform_data >> notify



