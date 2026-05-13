from plugins.utils.api_io import request_api
from plugins.utils.generate_token import get_token
from plugins.validations.validate_payload import validate_payload
from plugins.utils.file_io import write_json

def extract_from_api(run_id, path: str):
    #TODO: decide on how to handle malformed struct
    """
    create token for auth, request data and validate structure, fail DAG if malformed
    :param run_id:
    :param path:
    """
    token = get_token()

    data = request_api(token=token)

    issues = validate_payload(data)

    if issues:
        raise ValueError(
            f"[run_id={run_id}] Invalid payload: {issues}"
        )

    write_json(path=path, file_name=f"opensky_raw_{run_id}", data=data)
