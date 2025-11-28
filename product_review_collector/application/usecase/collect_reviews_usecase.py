from datetime import datetime
from typing import List, Mapping, Optional

from product_review_collector.application.port.review_crawler_port import ReviewCrawlerPort
from product_review_collector.domain.product_review import ProductReview


class CollectReviewsUseCase:
    """리뷰 수집 유스케이스: 입력 검증 후 크롤러 포트를 호출하고 결과를 도메인 모델로 정규화한다."""

    def __init__(self, crawler: ReviewCrawlerPort):
        self._crawler = crawler

    async def collect(self, product_url: str) -> List[ProductReview]:
        if not product_url or not product_url.strip():
            raise ValueError("product_url is required")

        raw = await self._crawler.fetch_reviews(product_url.strip())

        if isinstance(raw, Mapping):
            items = raw.items()
        elif isinstance(raw, list):
            # 리스트로 전달되는 경우 순서를 유지하며 인덱스를 키로 사용
            items = enumerate(raw, start=1)
        else:
            raise ValueError("unexpected crawler result type")

        def _parse_date(value: object) -> Optional[datetime]:
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                candidate = value.strip().rstrip(".")
                for fmt in ("%Y-%m-%d", "%y-%m-%d", "%y.%m.%d", "%y.%m.%d"):
                    try:
                        return datetime.strptime(candidate, fmt)
                    except ValueError:
                        continue
            return None

        reviews: List[ProductReview] = []
        for key, value in items:
            try:
                review_id = int(key)
            except (TypeError, ValueError):
                # 키를 숫자로 변환할 수 없는 경우 건너뜀
                continue

            content: Optional[str] = None
            grade: Optional[float] = None
            created_at: Optional[datetime] = None
            review_writer: Optional[str] = None

            if isinstance(value, Mapping):
                content = str(value.get("content") or "").strip()
                grade_raw = value.get("rating") if "rating" in value else value.get("grade")
                if grade_raw not in (None, ""):
                    try:
                        grade = float(grade_raw)
                    except (TypeError, ValueError):
                        grade = None
                review_writer = str(value.get("review_writer") or "").strip() or None
                created_at = _parse_date(value.get("created_at"))
            else:
                content = str(value or "").strip()

            if not content:
                continue

            reviews.append(
                ProductReview(
                    id=review_id,
                    content=content,
                    grade=grade,
                    review_writer=review_writer,
                    created_at=created_at,
                    source_url=product_url.strip(),
                )
            )

        if not reviews:
            raise ValueError("no reviews collected")

        # ID 기준 정렬로 일관된 응답 제공
        reviews.sort(key=lambda review: review.id)
        return reviews
