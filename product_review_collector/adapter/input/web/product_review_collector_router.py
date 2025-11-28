from fastapi import APIRouter, HTTPException

from product_review_collector.adapter.input.web.request.collect_reviews_request import (
    CollectReviewsRequest,
)
from product_review_collector.adapter.output.naver_crawler_adapter import (
    NaverCrawlerAdapter,
)
from product_review_collector.application.usecase.collect_reviews_usecase import (
    CollectReviewsUseCase,
)

router = APIRouter(tags=["product_review_collector"])
usecase = CollectReviewsUseCase(NaverCrawlerAdapter())


@router.post("/naver")
async def collect_reviews(request: CollectReviewsRequest):
    try:
        reviews = await usecase.collect(str(request.product_url))
        return {
            "items": [
                {
                    "id": review.id,
                    "content": review.content,
                    "rating": review.grade,
                    "writer": review.review_writer,
                    "created_at": review.created_at.date().isoformat() if review.created_at else None,
                }
                for review in reviews
            ]
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        # 이미 매핑된 HTTP 오류는 그대로 전달
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"review collector failed: {exc}")
