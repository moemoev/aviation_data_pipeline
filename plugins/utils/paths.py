import yaml

from pathlib import Path


with open("config/path_config.yaml", "r") as file:
    path = yaml.safe_load(file)

RAW_DIR = Path(path["paths"]["raw_storage"])
TRANSFORMED_DIR = Path(path["paths"]["transformed_storage"])
LOG_DIR = Path(path["paths"]["logs_storage"])



def raw_file(run_id: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    return RAW_DIR / f"opensky_raw_{run_id}.json"

def transformed_file(run_id: str) -> Path:
    TRANSFORMED_DIR.mkdir(parents=True, exist_ok=True)
    return TRANSFORMED_DIR / f"opensky_transformed_{run_id}.parquet"

def raw_log_file() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"opensky_raw_valid_log.jsonl"


def transformed_log_file() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"opensky_transformed_valid_log.jsonl"

