# from airflow import DAG
# from airflow.operators.python import PythonOperator
# import pendulum
#
# def test():
#     print("AIRFLOW DAG IS WORKING")
#
# with DAG(
#     dag_id="aviation_pipeline_test",
#     start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
#     schedule=None,
#     catchup=False,
# ) as dag:
#
#     task = PythonOperator(
#         task_id="print_test",
#         python_callable=test
#     )

import pandas as pd
import pathlib
import json
import pendulum
import requests

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG




def _get_raw_data():
    pathlib.Path("/tmp/data").mkdir(parents=True, exist_ok=True)


    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    data = response.json()


    with open("/tmp/data/raw_data.json", "w") as f:
        json.dump(data, f)


    return

def _expand_raw_data():
    pathlib.Path("/tmp/dataset").mkdir(parents=True, exist_ok=True)

    categories = ['icao240', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude',
                  'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
                  'squawk', 'spi', 'position_source']

    with open("/tmp/data/raw_data.json") as f:
        raw_data = json.load(f)

    aviation_expanded = pd.DataFrame(raw_data["states"])
    aviation_expanded.columns = categories[:aviation_expanded.shape[1]]
    aviation_expanded.insert(0, "time", raw_data["time"])


    aviation_expanded.to_csv("/tmp/dataset/aviation_expanded.csv", index=False)

    return

def notify():
    raw_data = pd.read_csv("/tmp/dataset/aviation_expanded.csv")

    total_rows = raw_data.shape[0]
    timestamp = raw_data["time"].unique()

    print(f"CSV Summary:")
    print(f"- Rows: {total_rows}")
    print(f"- time: {timestamp}")

    return

with DAG(
    dag_id="aviation_data_pipeline_v1",
    start_date=pendulum.today("UTC").add(days=-14),
    schedule=None,
):
    get_raw_data = PythonOperator(task_id="get_raw_data", python_callable=_get_raw_data)

    expand_raw_data = PythonOperator(task_id="expand_raw_data", python_callable=_expand_raw_data)

    notify = PythonOperator(task_id="notify", python_callable=notify)

    get_raw_data >> expand_raw_data >> notify



