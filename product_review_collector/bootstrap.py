from fastapi import FastAPI

from product_review_collector.adapter.input.web.product_review_collector_router import (
    get_collect_reviews_usecase,
    router as product_review_collector_router,
)
from product_review_collector.adapter.output.naver_crawler_adapter import NaverCrawlerAdapter
from product_review_collector.application.usecase.collect_reviews_usecase import CollectReviewsUseCase


def setup_product_review_collector(app: FastAPI) -> None:
    """Wire product review collector dependencies and routes."""
    crawler = NaverCrawlerAdapter()
    collect_usecase = CollectReviewsUseCase(crawler)

    app.dependency_overrides[get_collect_reviews_usecase] = lambda: collect_usecase
    app.include_router(product_review_collector_router, prefix="/product-reviews")
