import json
import pathlib
import pandas as pd

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