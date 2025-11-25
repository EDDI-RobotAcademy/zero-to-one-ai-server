from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from domain.review_summary import ReviewSummary
from application.usecase.preprocess_usecase import PreprocessUseCase
from adapter.output.text_cleaner_adapter import BeautifulSoupTextCleaner
from adapter.output.tokenizer_adapter import KoNLPyTokenizer

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


class PreprocessRequest(BaseModel):
    """전처리 요청"""
    reviews: dict[str, str]  # {"1": "리뷰 텍스트", ...}


class PreprocessResponse(BaseModel):
    """전처리 응답"""
    id: str
    original: str
    cleaned: str
    tokens: list[str]
    processed: str
    word_count: int


class StatisticsResponse(BaseModel):
    """통계 응답"""
    total_reviews: int
    processed_reviews: int
    avg_word_count: float
    min_word_count: int
    max_word_count: int


@router.post("/preprocess", response_model=list[PreprocessResponse])
async def preprocess_reviews(request: PreprocessRequest):
    """
    리뷰 전처리 API

    - HTML 태그 제거
    - 특수문자 정제
    - 형태소 분석
    - 불용어 제거
    """
    # 의존성 주입
    text_cleaner = BeautifulSoupTextCleaner()
    tokenizer = KoNLPyTokenizer()
    usecase = PreprocessUseCase(text_cleaner, tokenizer)

    # RawReview 객체 생성
    raw_reviews = ReviewSummary.from_json(request.reviews)

    # 전처리 실행
    processed_reviews = usecase.execute(raw_reviews)

    if not processed_reviews:
        raise HTTPException(status_code=400, detail="유효한 리뷰가 없습니다")

    # 통계 출력 (로그)
    stats = usecase.get_statistics(processed_reviews)
    print(f"📊 전처리 통계: {stats}")

    # Response 변환
    return [
        PreprocessResponse(
            id=r.id,
            original=r.original_text,
            cleaned=r.cleaned_text,
            tokens=r.tokens,
            processed=r.processed_text,
            word_count=r.word_count
        )
        for r in processed_reviews
    ]


@router.post("/preprocess/statistics", response_model=StatisticsResponse)
async def get_preprocess_statistics(request: PreprocessRequest):
    """전처리 통계만 반환"""
    text_cleaner = BeautifulSoupTextCleaner()
    tokenizer = KoNLPyTokenizer()
    usecase = PreprocessUseCase(text_cleaner, tokenizer)

    raw_reviews = ReviewSummary.from_json(request.reviews)
    processed_reviews = usecase.execute(raw_reviews)

    stats = usecase.get_statistics(processed_reviews)

    return StatisticsResponse(
        total_reviews=len(raw_reviews),
        processed_reviews=len(processed_reviews),
        avg_word_count=stats.get("avg_word_count", 0),
        min_word_count=stats.get("min_word_count", 0),
        max_word_count=stats.get("max_word_count", 0)
    )
