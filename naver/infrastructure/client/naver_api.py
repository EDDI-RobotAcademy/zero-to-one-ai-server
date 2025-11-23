from typing import Any, Dict

import requests

from config import naver_config


SHOP_SEARCH_PATH = "/v1/search/shop.json"


class NaverApiError(Exception):
    pass


def search_products(query: str, start: int = 1, display: int = 10) -> Dict[str, Any]:
    naver_config.validate_naver_config()

    url = f"{naver_config.NAVER_API_BASE}{SHOP_SEARCH_PATH}"
    headers = {
        "X-Naver-Client-Id": naver_config.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": naver_config.NAVER_CLIENT_SECRET,
    }
    params = {
        "query": query,
        "start": start,
        "display": display,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
    except requests.RequestException as exc:
        raise NaverApiError(f"Naver API request failed: {exc}") from exc

    if response.status_code != 200:
        raise NaverApiError(
            f"Naver API returned {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise NaverApiError("Failed to decode Naver API response as JSON") from exc
