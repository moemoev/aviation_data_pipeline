import pandas as pd
import yaml

with open("config/schema_config.yaml", "r") as file:
    schema = yaml.safe_load(file)


def transform_raw_data(raw_data: dict) -> pd.DataFrame:
    columns = schema["aviation_states"]["columns"]

    transformed_data = pd.DataFrame(raw_data['states'])
    transformed_data.columns = columns[:transformed_data.shape[1]]
    transformed_data.insert(0, 'time', raw_data['time'])

    return transformed_data