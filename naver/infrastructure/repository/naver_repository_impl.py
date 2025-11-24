import html
import re
from typing import List

from naver.application.port.naver_repository_port import NaverRepositoryPort
from naver.domain.product import Product
from naver.infrastructure.client import naver_api
from naver.infrastructure.client.naver_api import NaverApiError

TAG_RE = re.compile(r"<.*?>")


def _clean_title(title: str) -> str:
    return TAG_RE.sub("", html.unescape(title or ""))


class NaverRepositoryImpl(NaverRepositoryPort):
    def search_products(self, query: str, start: int = 1, display: int = 10) -> List[Product]:
        try:
            payload = naver_api.search_products(query=query, start=start, display=display)
        except NaverApiError:
            raise

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
