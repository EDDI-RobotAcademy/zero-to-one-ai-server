from fastapi import APIRouter
from pydantic import BaseModel
from review.domain.pdf_document import PdfDocument
from review.application.usecase.pdf_usecase import PdfUseCase
from review.adapter.output.pdf_adapter import PdfAdapter
from review.adapter.output.s3_upload_adapter import S3UploaderAdapter

review_router = APIRouter()

# PDF 생성 요청
class ReviewRequest(BaseModel):
    product_name: str
    category: str
    price: str
    summary: str
    positive_features: str
    negative_features: str
    keywords: list[str]

# 리뷰 요약 데이터를 기반으로 PDF 생성하고 S3 URL 반환
@review_router.post("/pdf")
def generate_pdf(data: ReviewRequest):
    report = PdfDocument(
        product_name=data.product_name,
        category=data.category,
        price=data.price,
        summary=data.summary,
        positive_features=data.positive_features,
        negative_features=data.negative_features,
        keywords=data.keywords
    )

    usecase = PdfUseCase(
        pdf_port=PdfAdapter(),
        storage_port=S3UploaderAdapter()
    )

    url = usecase.execute(report)

    return {"url": url}