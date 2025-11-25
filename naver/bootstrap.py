from fastapi import FastAPI

from naver.adapter.input.naver_router import get_naver_usecase, naver_router
from naver.adapter.output.naver_api_adapter import NaverSearchApiAdapter
from naver.application.usecase.naver_search_usecase import NaverSearchUseCase


def setup_module(app: FastAPI) -> None:
    """Wire Naver module into the FastAPI app."""
    search_adapter = NaverSearchApiAdapter()
    naver_usecase = NaverSearchUseCase(repository=search_adapter)

    app.dependency_overrides[get_naver_usecase] = lambda: naver_usecase
    app.include_router(naver_router, prefix="/naver")
