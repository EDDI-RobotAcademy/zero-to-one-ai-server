from fastapi import APIRouter, Depends, HTTPException

from naver.application.usecase.naver_usecase import NaverUseCase
from naver.infrastructure.client.naver_api import NaverApiError
from naver.infrastructure.repository.naver_repository_impl import NaverRepositoryImpl

naver_router = APIRouter()


def get_naver_usecase() -> NaverUseCase:
    repository = NaverRepositoryImpl()
    return NaverUseCase(repository)


@naver_router.get("/products")
def search_products(
    query: str,
    start: int = 1,
    display: int = 10,
    usecase: NaverUseCase = Depends(get_naver_usecase),
):
    try:
        products = usecase.search_products(query=query, start=start, display=display)
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
