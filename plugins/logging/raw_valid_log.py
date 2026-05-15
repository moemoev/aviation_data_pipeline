def create_raw_valid_log(run_id: str) -> dict:
    return {
        "run_id": run_id,
        "fetch_time_utc": None,
        "opensky_time": None,
        "fetch_success": False,
        "validation_success": False,
        "payload_saved": False,
        "validation_errors": [],
        "state_count": 0,
        "invalid_state_vectors": 0,
        "response_size_bytes": 0,
        "processing_duration_seconds": None,
        "pipeline_version": "v1"
    }

def update_log(log: dict, **kwargs) -> None:
    for key, value in kwargs.items():
        if key in log:
            log[key] = value
        else:
            raise KeyError(f"Invalid log field: {key}")