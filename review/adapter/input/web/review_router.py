from fastapi import APIRouter, Depends

from product_review_collector.adapter.input.web.product_review_collector_router import (
    get_collect_reviews_usecase,
)
from product_review_collector.application.usecase.collect_reviews_usecase import (
    CollectReviewsUseCase,
)
from review.adapter.input.web.request.SummaryRequest import SummaryRequest
from review.adapter.input.web.response.SummaryResponse import ProductSummary, SummaryResponse
from review.application.usecase.pdf_usecase import PdfUseCase
from review.application.usecase.preprocess_usecase import PreprocessUseCase
from review.application.usecase.summarize_usecase import SummarizeUseCase
from review.domain.pdf_document import PdfDocument

review_router = APIRouter()


def get_preprocess_usecase() -> PreprocessUseCase:
    # Provided via dependency override in review.bootstrap.setup_module
    raise RuntimeError("PreprocessUseCase dependency is not wired")


def get_summarize_usecase() -> SummarizeUseCase:
    # Provided via dependency override in review.bootstrap.setup_module
    raise RuntimeError("SummarizeUseCase dependency is not wired")


def get_pdf_usecase() -> PdfUseCase:
    # Provided via dependency override in review.bootstrap.setup_module
    raise RuntimeError("PdfUseCase dependency is not wired")


@review_router.post("/summary", response_model=SummaryResponse)
async def analyze_product(
    data: SummaryRequest,
    collector: CollectReviewsUseCase = Depends(get_collect_reviews_usecase),
    preprocess_usecase: PreprocessUseCase = Depends(get_preprocess_usecase),
    summarize_usecase: SummarizeUseCase = Depends(get_summarize_usecase),
    pdf_usecase: PdfUseCase = Depends(get_pdf_usecase),
):
    # 1. 크롤링
    collected_reviews = await collector.collect(str(data.info_url))
    raw_reviews = [review.content for review in collected_reviews]

    # 2. 전처리
    preprocessed_data = preprocess_usecase.execute(raw_reviews)
    preprocessed_text = " ".join(item["text"] for item in preprocessed_data["clean_reviews"])

    # 3. 요약
    summary_result = summarize_usecase.summarize_review(data.name, preprocessed_text)

    # 4. PDF 생성 + S3 업로드
    pdf_document = PdfDocument(
        name=data.name,
        price=data.price,
        summary=summary_result["summary"],
        positive_features=summary_result["positive_features"],
        negative_features=summary_result["negative_features"],
        keywords=summary_result["keywords"],
    )

    pdf_result = pdf_usecase.execute(pdf_document)

    return SummaryResponse(
        product_summary=ProductSummary(
            name=data.name,
            price=data.price,
            summary=summary_result["summary"],
            positive_features=summary_result["positive_features"],
            negative_features=summary_result["negative_features"],
            keywords=summary_result["keywords"],
        ),
        pdf_url=pdf_result["url"],
    )


