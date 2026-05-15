import pandas as pd
import yaml

from plugins.utils.file_io import read_json, write_parquet, write_jsonl
from plugins.utils.paths import raw_file, transformed_file, transformed_log_file
from plugins.validations.validate_schema import validate_dataframe_schema


with open("config/schema_config.yaml", "r") as file:
    schema = yaml.safe_load(file)


def transform_raw_data(run_id):

    path_raw = raw_file(run_id=run_id)
    raw_data = read_json(path=path_raw)

    columns = schema["aviation_states"]["columns"]

    transformed_data = pd.DataFrame(raw_data['states'])
    transformed_data.columns = columns[:transformed_data.shape[1]]
    transformed_data.insert(0, 'time', raw_data['time'])

    validation = validate_dataframe_schema(df=transformed_data)

    log_entry = {
        "run_id": run_id,
        "status": 'valid'
    }

    if not validation['valid']:
        log_entry['status'] = 'invalid'
        log_entry['errors'] = validation['errors']

    path_logs = transformed_log_file()
    write_jsonl(path=path_logs,log_entry=log_entry)

    path_transformed = transformed_file(run_id)
    write_parquet(path=path_transformed, data=transformed_data)

def cleanse_data(staged_data: pd.DataFrame) -> pd.DataFrame:
    drop_cols = ["sensors", "spi", "position_source"]
    strip_cols = ["icao24", "callsign", "origin_country"]

    cleaned_data = staged_data

    cleaned_data[strip_cols] = (
        cleaned_data[strip_cols]
        .astype(str)
        .apply(lambda col: col.str.strip())
    )

    cleaned_data = (
        cleaned_data
        .drop(columns=drop_cols)
        .drop_duplicates()
        .dropna(subset=["icao24", "callsign"])
    )

    return cleaned_data