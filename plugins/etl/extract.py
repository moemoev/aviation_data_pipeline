from plugins.utils.api_io import request_api
from plugins.utils.generate_token import get_token
from plugins.validations.validate_payload import validate_payload
from plugins.utils.file_io import write_json
from plugins.utils.paths import raw_file

def extract_from_api(run_id):
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

    path = raw_file(run_id=run_id)
    write_json(path=path, data=data)
