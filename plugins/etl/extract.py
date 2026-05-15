import json
import time
import pandas as pd

from datetime import datetime, UTC
from sqlalchemy import create_engine

from plugins.utils.api_io import request_api
from plugins.utils.generate_token import get_token
from plugins.validations.validate_payload import validate_payload
from plugins.utils.file_io import write_json, write_jsonl
from plugins.utils.paths import raw_file, raw_log_file
from plugins.utils.connections import get_postgres_conn_str
from plugins.logging.raw_valid_log import create_raw_valid_log, update_log




def extract_from_api(run_id):
    #TODO: decide on how to handle malformed struct
    """
    create token for auth, request data and validate structure, fail DAG if malformed
    :param run_id:
    :param path:
    """

    log_entry = None
    start = time.perf_counter()

    try:
        log_entry = create_raw_valid_log(run_id=run_id)

        token = get_token()

        data = request_api(token=token)
        update_log(log=log_entry,
            state_count=len(data.get("states", [])),
            invalid_state_vectors=sum(len(s) != 17 for s in data.get("states", [])),
            fetch_time_utc=datetime.now(UTC).isoformat(),
            opensky_time=data.get("time"),
            fetch_success=True,
            response_size_bytes=len(json.dumps(data).encode("utf-8"))
        )

        issues = validate_payload(data)


        if issues:
            update_log(log_entry, validation_errors=issues)

            raise ValueError(f"[run_id={run_id}] Invalid payload: {issues}")

        update_log(log_entry, validation_success=True)

        path = raw_file(run_id=run_id)
        write_json(path=path, data=data)

        update_log(log_entry, payload_saved=True)

    finally:
        update_log(
            log_entry,
            processing_duration_seconds=round(time.perf_counter() - start,4)
        )
        path_log = raw_log_file()
        write_jsonl(path=path_log, log_entry=log_entry)


def extract_from_db(schema: str) -> pd.DataFrame:
    engine = create_engine(get_postgres_conn_str())

    staged_data = pd.read_sql(
        f"SELECT * FROM {schema}.data", con=engine
    )

    return staged_data
