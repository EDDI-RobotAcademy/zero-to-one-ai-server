import os

from fastapi import FastAPI


def _is_enabled(env_var: str) -> bool:
    return os.getenv(env_var, "false").lower() in {"1", "true", "yes", "on"}


def setup_product_review_collector(app: FastAPI) -> None:
    """Wire product review collector routers into the FastAPI app."""
    if not _is_enabled("ENABLE_PRODUCT_REVIEW_COLLECTOR"):
        return

    from product_review_collector.adapter.input.web.product_review_collector_router import (  # noqa: WPS433,E501
        router as product_review_collector_router,
    )

    app.include_router(
        product_review_collector_router,
        prefix="/product-review-collector",
    )
