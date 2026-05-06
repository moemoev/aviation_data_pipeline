import requests
from plugins.utils.logger import setup_logger

logger = setup_logger(name="request_api")

def request_api(url: str)-> dict:
    logger.info(f"Requesting data from API: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        logger.info(f"Successfully fetched data from API: {url}")
        return data

    except Exception:
        logger.exception(f"Api request failed for {url}")
        raise


