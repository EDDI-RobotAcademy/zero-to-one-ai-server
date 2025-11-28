from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from review.domain.pdf_document import PdfDocument
from review.application.usecase.pdf_usecase import PdfUseCase
from review.application.usecase.preprocess_usecase import PreprocessUseCase
from review.adapter.output.pdf_adapter import PdfAdapter
from review.adapter.output.s3_upload_adapter import S3UploaderAdapter
from typing import List, Optional
review_router = APIRouter()
preprocess_usecase = PreprocessUseCase()

# PDF 생성 요청
class ReviewRequest(BaseModel):
    product_name: str
    category: str
    price: str
    summary: str
    positive_features: str
    negative_features: str
    keywords: list[str]

# 전처리 테스트 요청 (리뷰 목록이 없으면 샘플 데이터를 사용)
class PreprocessRequest(BaseModel):
    reviews: Optional[List[str]] = None

# 샘플 리뷰 데이터
SAMPLE_REVIEWS = [
    "가방 디자인이 너무 예뻐요, 친구들이 다 칭찬했어요.",
    "가죽 질감이 고급스럽고 튼튼해요.",
    "스트랩 길이가 조금 짧아서 어깨에 맞지 않아요.",
    "수납 공간이 넓어서 짐이 많이 들어갑니다.",
    "지퍼가 부드럽게 잘 열리고 닫혀요.",
    "가격 대비 품질이 만족스러워요.",
    "배송이 빨라서 좋았어요.",
    "포장이 조금 부실해서 걱정됐습니다.",
    "가방이 예상보다 가벼워서 들고 다니기 편합니다.",
    "색상이 사진과 조금 달라요.",
    "내부 포켓이 많아서 소지품 정리하기 좋아요.",
    "끈 마감이 깔끔하지 못해 아쉬워요.",
    "여행용으로 적당한 사이즈라 편리합니다.",
    "가죽 냄새가 조금 강하지만 시간이 지나면 괜찮아요.",
    "디자인이 세련되어서 일상용으로 좋아요.",
    "손잡이가 튼튼하게 제작되어 있어 안심돼요.",
    "가방 무게가 좀 무겁습니다.",
    "주머니 위치가 편리해서 자주 쓰는 물건 넣기 좋아요.",
    "끈 길이 조절이 어려워요.",
    "색상이 화면과 거의 동일해서 만족스러워요.",
    "가죽이 부드러워서 촉감이 좋아요.",
    "지퍼가 잘 걸려서 열다가 힘들었어요.",
    "여행, 출퇴근 둘 다 쓰기 적당한 사이즈입니다.",
    "포켓이 많아 물건 정리하기 편하지만, 조금 복잡해요.",
    "디자인이 깔끔하고 어떤 옷에도 잘 어울립니다.",
    "어깨끈이 조금 얇아서 장시간 착용하면 불편합니다.",
    "가방 내부가 생각보다 넓고 수납력이 좋아요.",
    "마감이 정교하고 전체적으로 퀄리티가 좋습니다.",
    "배송이 늦어서 조금 아쉬웠습니다.",
    "가방 색상이 다양한 스타일에 잘 어울려서 만족스러워요.",
]

# 전처리만 실행해 결과를 확인하는 엔드포인트
""" 테스트 시 POST /reviews/preprocess-test body
{
  "reviews": [
    "가방 디자인이 예뻐요오오오오 완전전 굿이욤욤욤",
    "스트랩이 좀 짧음음음ㅜㅜㅜ"
  ]
}"""

@review_router.post("/preprocess-test")
def preprocess_reviews(data: PreprocessRequest):
    input_reviews = data.reviews if data.reviews else SAMPLE_REVIEWS
    preprocess_result = preprocess_usecase.execute(input_reviews)

    return {
        "preprocessed": preprocess_result["clean_reviews"],
        "stats": preprocess_result["stats"],
        "json_payload": preprocess_result["json_payload"],
    }

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