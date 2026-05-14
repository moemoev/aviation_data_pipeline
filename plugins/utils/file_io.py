import json
import pathlib
import pandas as pd

from plugins.utils.logger import setup_logger

logger = setup_logger(name="file_io")

# --------------------
# READ FUNCTIONS
# --------------------

def read_json(path: pathlib.Path)-> dict:
    """
    read a JSON file

    """

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        with path.open("r") as f:
            data = json.load(f)

            logger.info(f"Successfully read JSON file from {path}")
            return data
    except Exception:
        logger.exception(f"Failed to read JSON (possibly corrupted) from {path}")
        raise



def read_parquet(path: pathlib.Path)-> pd.DataFrame:
    """
    Read a Parquet file

    """

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_parquet(path)

        logger.info(f"Successfully read parquet file from {path}")
        return df

    except Exception:
        logger.exception(f"Failed to read Parquet (possibly corrupted) from {path}")
        raise

# --------------------
# WRITE FUNCTIONS
# --------------------

def write_json(path: pathlib.Path, data: dict)-> None:
    """
    Write data to a JSON file

    """

    try:
        with path.open("w") as f:
            json.dump(data, f)

            logger.info(f"Successfully wrote JSON file at: {path}")

    except Exception:
        logger.exception(f"Failed to write JSON file at {path}")
        raise

def write_parquet(path: pathlib.Path, data: pd.DataFrame)-> None:
    """
    Write data to a Parquet file

    """

    try:
        data.to_parquet(path, index=False)

        logger.info(f"Successfully wrote Parquet file at: {path}")

    except Exception:
        logger.exception(f"Failed to write Parquet file at {path}")
        raise

