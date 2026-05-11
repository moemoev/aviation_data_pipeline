import pandas as pd
import yaml

from plugins.utils.file_io import read_json, write_csv
from plugins.validations.validate_schema import validate_dataframe_schema


with open("config/schema_config.yaml", "r") as file:
    schema = yaml.safe_load(file)


def transform_raw_data(run_id, path_raw: str, path_transformed: str, path_custom_logs: str):

    source_file_path = f"{path_raw}/opensky_raw_{run_id}.json"

    raw_data = read_json(source_file_path)

    columns = schema["aviation_states"]["columns"]

    transformed_data = pd.DataFrame(raw_data['states'])
    transformed_data.columns = columns[:transformed_data.shape[1]]
    transformed_data.insert(0, 'time', raw_data['time'])


    validate_dataframe_schema(transformed_data, path=path_custom_logs)

    write_csv(path=path_transformed, file_name=f"opensky_transformed_{run_id}", data=transformed_data)