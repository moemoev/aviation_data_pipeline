import requests
from plugins.utils.logger import setup_logger

logger = setup_logger(name="request_api")

def request_api(url: str, token:str)-> dict:
    """
    Request API

    """
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


