from typing import Protocol, runtime_checkable


@runtime_checkable
class ReviewCrawlerPort(Protocol):
    """포트: 상품 리뷰를 수집하는 외부 크롤러 인터페이스."""

    async def fetch_reviews(self, product_url: str) -> dict:
        """주어진 상품 URL에서 리뷰 데이터를 비동기적으로 수집한다."""
