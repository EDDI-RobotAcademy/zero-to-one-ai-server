from typing import List

from naver.application.port.naver_search_port import NaverSearchPort
from naver.domain.product import Product


class NaverSearchUseCase:
    def __init__(self, repository: NaverSearchPort):
        self.repository = repository

    def search_products(
        self,
        query: str,
        start: int = 1,
        display: int = 10,
    ) -> List[Product]:
        if not query or not query.strip():
            raise ValueError("query is required")

        safe_start = max(1, start)
        safe_display = min(max(1, display), 100)  # Naver API limit is 100

        search_query = query.strip()
        # Accumulate results until we have enough SmartStore items (or we run out)
        collected: List[Product] = []
        api_start = safe_start
        # Ask for a slightly larger page to improve chances of filling the target count
        page_size = min(max(safe_display * 2, safe_display), 100)
        max_api_start = 1000  # Naver Shopping API supports start up to 1000

        while len(collected) < safe_start + safe_display - 1 and api_start <= max_api_start:
            products = self.repository.search_products(
                query=search_query,
                start=api_start,
                display=page_size,
            )

            if not products:
                break

            products = [
                product
                for product in products
                if "smartstore.naver.com" in (product.info_url or "")
            ]

            collected.extend(products)

            # Move the API start forward by the page_size to avoid requesting the same slice
            api_start += page_size

        # Apply user-facing start/display over the filtered list
        start_index = safe_start - 1
        end_index = start_index + safe_display
        return collected[start_index:end_index]
