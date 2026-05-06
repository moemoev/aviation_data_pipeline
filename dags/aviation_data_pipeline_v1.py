import pandas as pd
import yaml
import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from airflow.operators.python import get_current_context

from plugins.utils.api_io import request_api
from plugins.utils.file_io import read_json, read_csv, write_json, write_csv

with open("config/api_config.yaml", "r") as file:
    config = yaml.safe_load(file)

with open("config/path_config.yaml", "r") as file:
    path = yaml.safe_load(file)

with open("config/schema_config.yaml", "r") as file:
    schema = yaml.safe_load(file)

PATH_RAW = path['paths']['raw_storage']
PATH_TRANSFORMED = path['paths']['transformed_storage']

start = pendulum.datetime(2026 , 4, 27 , 13, 59, tz="Europe/Berlin")
# end = start.add(minutes=2)



def _extract_data(ti):
    run_id = ti.run_id.replace(":", "_")
    #data = {"states": [], "time": 0}
    data = request_api(url=config['aviation_api'])

    # write data to file
    write_json(path=PATH_RAW, file_name=f"opensky_raw_{run_id}", data=data)

    return run_id

def _transform_data(ti):

    run_id = ti.xcom_pull(task_ids="extract_data")

    columns = schema["aviation_states"]["columns"]

    source_file_path = f"{PATH_RAW}/opensky_raw_{run_id}.json"
    raw_data = read_json(source_file_path)

    transformed_data = pd.DataFrame(raw_data['states'])
    transformed_data.columns = columns[:transformed_data.shape[1]]
    transformed_data.insert(0, 'time', raw_data['time'])

    write_csv(path=PATH_TRANSFORMED, file_name=f"opensky_transformed_{run_id}", data=transformed_data)


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

    notify = PythonOperator(task_id="notify", python_callable=notify)

    extract_data >> transform_data >> notify



