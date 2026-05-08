import json
import pathlib
import pandas as pd

from plugins.utils.logger import setup_logger
from plugins.utils.paths import build_path

logger = setup_logger(name="file_io")

# --------------------
# READ FUNCTIONS
# --------------------

def read_json(path: str)-> dict:
    """
    read a JSON file

    """
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        with open(path, "r") as f:
            data = json.load(f)

            logger.info(f"Successfully read JSON file from {path}")
            return data
    except Exception:
        logger.exception(f"Failed to read JSON (possibly corrupted) from {path}")
        raise



def read_csv(path: str)-> pd.DataFrame:
    """
    Read a CSV file

    """
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_csv(path)

        logger.info(f"Successfully read CSV file from {path}")
        return df

    except Exception:
        logger.exception(f"Failed to read CSV (possibly corrupted) from {path}")
        raise

# --------------------
# WRITE FUNCTIONS
# --------------------

def write_json(path: str, file_name: str, data: dict)-> None:
    """
    Write data to a JSON file

    """

    full_path = build_path(path, file_name, "json")

    try:
        with open(full_path, "w") as f:
            json.dump(data, f)

            logger.info(f"Successfully wrote JSON file at: {full_path}")

    except Exception:
        logger.exception(f"Failed to write JSON file at {full_path}")
        raise

def write_csv(path: str, file_name: str, data: pd.DataFrame)-> None:
    """
    Write data to a CSV file

    """
    full_path = build_path(path, file_name, "csv")

    try:
        data.to_csv(full_path, index=False)

        logger.info(f"Successfully wrote CSV file at: {full_path}")

    except Exception:
        logger.exception(f"Failed to write CSV file at {full_path}")
        raise

