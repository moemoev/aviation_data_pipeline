import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG


from plugins.etl.extract import extract_from_db
from plugins.etl.transform import cleanse_data
from plugins.etl.load import load_data

start = pendulum.datetime(2026 , 4, 27 , 13, 59, tz="Europe/Berlin")
#end = start.add(minutes=60)



def _clean_data():
    staged_data = extract_from_db(schema="raw_layer")

    cleaned_data = cleanse_data(staged_data=staged_data)

    load_data(data=cleaned_data, schema="staging_layer")

with DAG(
    dag_id="clean_data_v1",
    start_date=start,
    #end_date=end,
    schedule=None, #"*/5 * * * *",
    catchup=False,
):
    clean_data = PythonOperator(task_id="clean_data", python_callable=_clean_data)

    clean_data