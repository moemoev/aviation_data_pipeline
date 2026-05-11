import requests
import yaml
from plugins.utils.logger import setup_logger

logger = setup_logger(name="request_api")

with open("config/api_config.yaml", "r") as file:
    config = yaml.safe_load(file)

def request_api(token:str)-> dict:
    """
    Request API

    """
    url = get_request_string()

    logger.info(f"Requesting data from API: {url}")

    headers = {"Authorization": f"Bearer {token}"}



    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        logger.info(f"Successfully fetched data from API: {url}")
        logger.info(f"Authorization header set: Bearer <token present>")
        logger.info(f"Auth request response status: {response.status_code}")

        return data

    except Exception:
        logger.exception(f"Api request failed for {url}")
        raise

def get_request_string() -> str:

    logger.info(f"Building Request string: Box Values for Germany")

    try:
        request_string = (f"{config['aviation_api']}?"
                          f"lamin={config['la_min']}&"
                          f"lomin={config['lo_min']}&"
                          f"lamax={config['la_max']}&"
                          f"lomax={config['lo_max']}"
                          )

        logger.info(f"API REQUEST URL: {request_string}")

        return request_string

    except Exception:
        logger.exception(f"Building request string failed.")
        raise

