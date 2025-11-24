from typing import List

from naver.application.port.naver_repository_port import NaverRepositoryPort
from naver.domain.product import Product


class NaverUseCase:
    def __init__(self, repository: NaverRepositoryPort):
        self.repository = repository

    def search_products(self, query: str, start: int = 1, display: int = 10) -> List[Product]:
        if not query or not query.strip():
            raise ValueError("query is required")

        safe_start = max(1, start)
        safe_display = min(max(1, display), 100)  # Naver API limit is 100

        return self.repository.search_products(
            query=query.strip(), start=safe_start, display=safe_display
        )
