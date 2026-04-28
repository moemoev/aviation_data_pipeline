import json
import pathlib
import pandas as pd

from plugins.utils.logger import setup_logger

logger = setup_logger(name="file_io")

def read_json(path: str)-> dict:
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to read JSON (possibly corrupted): {path}") from e

    return data


def read_csv(path: str)-> pd.DataFrame:
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        return pd.read_csv(path)
    except FileNotFoundError as e:
        raise ValueError(f"Failed to read CSV (possibly corrupted): {path}") from e

def write_json(path: str, file_name: str, data: dict)-> None:

    dir_path = pathlib.Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)

    full_path = dir_path / f"{file_name}.json"

    try:
        with open(full_path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        raise IOError(f"Failed to write JSON file at {full_path}: {e}")

def write_csv(path: str, file_name: str, data: pd.DataFrame)-> None:
    dir_path = pathlib.Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)

    full_path = dir_path / f"{file_name}.csv"

    try:
        data.to_csv(full_path, index=False)
    except Exception as e:
        raise IOError(f"Failed to write CSV file at {full_path}: {e}")

