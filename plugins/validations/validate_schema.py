import pandas as pd

from pandera.errors import SchemaErrors
from plugins.validations.schema import aviation_schema
from plugins.utils.logger import setup_logger
from plugins.utils.file_io import write_json

logger = setup_logger("validate_dataframe_schema")
#TODO: don't forget the path for the logs you are not using at all right now! at least not properly
def validate_dataframe_schema(df: pd.DataFrame, path=None) -> pd.DataFrame:
    """
    Validate the dataframe schema
    """
    logger.info(f"Validating dataframe schema")

    try:
        return aviation_schema.validate(df, lazy=True)


    except SchemaErrors as e:
        data = e.failure_cases.to_json(orient="records")
        write_json(path, "logs_test", data)
        logger.warning(f"Schema error: {e.failure_cases}")

    return df