import pandas as pd

from pandera.errors import SchemaErrors
from plugins.validations.schema import aviation_schema
from plugins.utils.logger import setup_logger
from plugins.utils.file_io import write_json

logger = setup_logger("validate_dataframe_schema")
#TODO: don't forget the path for the logs you are not using at all right now! at least not properly
def validate_dataframe_schema(df: pd.DataFrame) -> dict:
    """
    Validate the dataframe schema
    """
    logger.info(f"Validating dataframe schema")

    try:
        aviation_schema.validate(check_obj=df, lazy=True)

        return {
            "valid": True,
            "errors": []
        }

    except SchemaErrors as e:
        data = e.failure_cases.to_json(orient="records")


        logger.warning(f"Schema error: {e.failure_cases}")

        return {
            "valid": False,
            "errors": e.failure_cases.to_dict(orient="records")
        }