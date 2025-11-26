from fastapi import APIRouter, Depends, HTTPException

from naver.adapter.output.naver_api_adapter import NaverApiError
from naver.application.usecase.naver_search_usecase import NaverSearchUseCase

naver_router = APIRouter()


def get_naver_usecase() -> NaverSearchUseCase:
    # Provided via dependency override in composition root (app/main.py)
    raise RuntimeError("NaverSearchUseCase dependency is not wired")


@naver_router.get("/products")
def search_products(
    query: str,
    start: int = 1,
    display: int = 10,
    smartstore_only: bool = True,
    usecase: NaverSearchUseCase = Depends(get_naver_usecase),
):
    try:
        products = usecase.search_products(
            query=query,
            start=start,
            display=display,
            smartstore_only=smartstore_only,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except NaverApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return {
        "items": [
            {
                "name": product.name,
                "thumbnail_url": product.thumbnail_url,
                "price": product.price,
                "info_url": product.info_url,
            }
            for product in products
        ]
    }
