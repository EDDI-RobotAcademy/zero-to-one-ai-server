from fastapi import FastAPI

from config.openai.config import openai_client
from product_review_crawling_agents.application.usecase.product_review_crawling_agents_usecase import (
    ProductReviewAgentsUseCase,
)
from review.adapter.input.web.review_router import (
    get_pdf_usecase,
    get_preprocess_usecase,
    get_review_crawling_usecase,
    get_summarize_usecase,
    review_router,
)
from review.adapter.output.llm_adapter import LLMAdapter
from review.adapter.output.pdf_adapter import PdfAdapter
from review.adapter.output.s3_upload_adapter import S3UploaderAdapter
from review.application.usecase.pdf_usecase import PdfUseCase
from review.application.usecase.preprocess_usecase import PreprocessUseCase
from review.application.usecase.summarize_usecase import SummarizeUseCase
from review.infrastructure.client.openai_client import OpenAIClient


def setup_module(app: FastAPI) -> None:
    """Wire review module dependencies and routes."""
    openai_client_adapter = OpenAIClient(openai_client)

    crawling_usecase = ProductReviewAgentsUseCase.get_instance()
    preprocess_usecase = PreprocessUseCase()
    summarize_usecase = SummarizeUseCase(LLMAdapter(openai_client_adapter))
    pdf_usecase = PdfUseCase(PdfAdapter(), S3UploaderAdapter())

    app.dependency_overrides[get_review_crawling_usecase] = lambda: crawling_usecase
    app.dependency_overrides[get_preprocess_usecase] = lambda: preprocess_usecase
    app.dependency_overrides[get_summarize_usecase] = lambda: summarize_usecase
    app.dependency_overrides[get_pdf_usecase] = lambda: pdf_usecase

    app.include_router(review_router, prefix="/review")
