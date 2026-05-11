from plugins.utils.api_io import request_api
from plugins.utils.generate_token import get_token
from plugins.utils.file_io import write_json

def extract_from_api(run_id, path: str):

    token = get_token()

    data = request_api(token=token)

    write_json(path=path, file_name=f"opensky_raw_{run_id}", data=data)