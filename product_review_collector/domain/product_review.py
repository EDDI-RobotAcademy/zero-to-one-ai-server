from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ProductReview:
    """상품 리뷰 도메인 모델."""

    id: int
    content: str
    product_domain: Optional[str] = None
    product_name: Optional[str] = None
    review_writer: Optional[str] = None
    grade: Optional[float] = None
    created_at: Optional[datetime] = None
    source_url: Optional[str] = None
