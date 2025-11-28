from fastapi import APIRouter, Depends, HTTPException

from product_review_collector.adapter.input.web.request.collect_reviews_request import (
    CollectReviewsRequest,
)
from product_review_collector.application.usecase.collect_reviews_usecase import (
    CollectReviewsUseCase,
)

router = APIRouter(tags=["product_review_collector"])


def get_collect_reviews_usecase() -> CollectReviewsUseCase:
    # Provided via dependency override in product_review_collector.bootstrap
    raise RuntimeError("CollectReviewsUseCase dependency is not wired")


@router.post("/naver")
async def collect_reviews(
    request: CollectReviewsRequest,
    usecase: CollectReviewsUseCase = Depends(get_collect_reviews_usecase),
):
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
