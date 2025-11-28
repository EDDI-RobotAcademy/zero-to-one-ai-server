from abc import ABC, abstractmethod
from typing import List

from naver.domain.product import Product


class NaverSearchPort(ABC):
    @abstractmethod
    def search_products(
        self,
        query: str,
        start: int = 1,
        display: int = 10,
    ) -> List[Product]:
        """Search products by keyword using Naver Shopping API."""
        raise NotImplementedError
