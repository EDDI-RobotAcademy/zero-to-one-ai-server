from fastapi import APIRouter

from product_review_crawling_agents.application.usecase.product_review_crawling_agents_usecase import \
    ProductReviewAgentsUseCase
from review.adapter.input.web.request.SummaryRequest import SummaryRequest
from review.adapter.input.web.response.SummaryResponse import SummaryResponse, ProductSummary
from review.adapter.output.llm_adapter import LLMAdapter
from review.adapter.output.pdf_adapter import PdfAdapter
from review.adapter.output.s3_upload_adapter import S3UploaderAdapter
from review.application.usecase.preprocess_usecase import PreprocessUseCase
from review.application.usecase.pdf_usecase import PdfUseCase
from review.application.usecase.summarize_usecase import SummarizeUseCase
from review.domain.pdf_document import PdfDocument
from review.infrastructure.client.openai_client import OpenAIClient
from config.openai.config import openai_client

review_router = APIRouter()
client = OpenAIClient(openai_client)

summarizeUsecase = SummarizeUseCase(LLMAdapter(client))
naverReviewCrawlingUsecase = ProductReviewAgentsUseCase()
preprocessUsecase = PreprocessUseCase()
pdfUsecase = PdfUseCase(PdfAdapter(), S3UploaderAdapter())


@review_router.post("/summary", response_model=SummaryResponse)
async def analyze_product(data: SummaryRequest):
    # 1. 크롤링
    raw_reviews = await naverReviewCrawlingUsecase.crawling_naver_review_agents(data.info_url)

    # 2. 전처리
    preprocessed_data = preprocessUsecase.execute(raw_reviews)
    preprocessed_text = " ".join([item["text"] for item in preprocessed_data["clean_reviews"]])

    # 3. 요약
    summary_result = summarizeUsecase.summarize_review(data.name, preprocessed_text)

    # 4. PDF 생성 + S3 업로드
    pdf_document = PdfDocument(
        name=data.name,
        price=data.price,
        summary=summary_result["summary"],
        positive_features=summary_result["positive_features"],
        negative_features=summary_result["negative_features"],
        keywords=summary_result["keywords"]
    )

    pdf_result = pdfUsecase.execute(pdf_document)

    return SummaryResponse(
        product_summary=ProductSummary(
            name=data.name,
            price=data.price,
            summary=summary_result["summary"],
            positive_features=summary_result["positive_features"],
            negative_features=summary_result["negative_features"],
            keywords=summary_result["keywords"]
        ),
        pdf_url=pdf_result["url"]
    )



