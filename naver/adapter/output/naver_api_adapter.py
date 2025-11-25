import html
import re
from typing import Any, Dict, List

import requests

from config import naver_config
from naver.application.port.naver_search_port import NaverSearchPort
from naver.domain.product import Product

SHOP_SEARCH_PATH = "/v1/search/shop.json"
_TAG_RE = re.compile(r"<.*?>")


class NaverApiError(Exception):
    pass


def _request_search_products(query: str, start: int = 1, display: int = 10) -> Dict[str, Any]:
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


def _clean_title(title: str) -> str:
    return _TAG_RE.sub("", html.unescape(title or ""))


class NaverSearchApiAdapter(NaverSearchPort):
    """Outbound adapter: call Naver Shopping API and map to domain products."""

    def search_products(self, query: str, start: int = 1, display: int = 10) -> List[Product]:
        payload = _request_search_products(query=query, start=start, display=display)

        items = payload.get("items", []) if isinstance(payload, dict) else []

        products: List[Product] = []
        for item in items:
            price_str = item.get("lprice") or item.get("hprice") or "0"
            try:
                price = int(price_str)
            except (TypeError, ValueError):
                price = 0

            products.append(
                Product(
                    name=_clean_title(item.get("title", "")),
                    thumbnail_url=item.get("image", ""),
                    price=price,
                    info_url=item.get("link", ""),
                )
            )

        return products
