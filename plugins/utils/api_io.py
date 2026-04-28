import requests


def request_api(url: str)-> dict:

    try:
        response = requests.get(url)
        data = response.json()
        response.raise_for_status()
        return data
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Api request failed for {url}: {e}")


