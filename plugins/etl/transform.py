import pandas as pd
import yaml

from plugins.utils.file_io import read_json, write_parquet
from plugins.utils.paths import raw_file, transformed_file, log_file
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

    path_logs = log_file(run_id=run_id)
    validate_dataframe_schema(path=path_logs, df=transformed_data)

    path_transformed = transformed_file(run_id)
    write_parquet(path=path_transformed, data=transformed_data)