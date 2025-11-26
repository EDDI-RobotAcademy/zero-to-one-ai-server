from fastapi import APIRouter
import json
from review.adapter.output.llm_adapter import LLMAdapter
from review.application.usecase.summarize_usecase import SummarizeUseCase
from review.infrastructure.client.openai_client import OpenAIClient
from config.openai.config import openai_client

review_router = APIRouter()
client = OpenAIClient(openai_client)
summerizeUsecase = SummarizeUseCase(LLMAdapter(client))


@review_router.get("/go")
def test_review():

    preprocessed_reviews = [
        {"text": "가방 디자인이 너무 예뻐요, 친구들이 다 칭찬했어요."},
        {"text": "가죽 질감이 고급스럽고 튼튼해요."},
        {"text": "스트랩 길이가 조금 짧아서 어깨에 맞지 않아요."},
        {"text": "수납 공간이 넓어서 짐이 많이 들어갑니다."},
        {"text": "지퍼가 부드럽게 잘 열리고 닫혀요."},
        {"text": "가격 대비 품질이 만족스러워요."},
        {"text": "배송이 빨라서 좋았어요."},
        {"text": "포장이 조금 부실해서 걱정됐습니다."},
        {"text": "가방이 예상보다 가벼워서 들고 다니기 편합니다."},
        {"text": "색상이 사진과 조금 달라요."},
        {"text": "내부 포켓이 많아서 소지품 정리하기 좋아요."},
        {"text": "끈 마감이 깔끔하지 못해 아쉬워요."},
        {"text": "여행용으로 적당한 사이즈라 편리합니다."},
        {"text": "가죽 냄새가 조금 강하지만 시간이 지나면 괜찮아요."},
        {"text": "디자인이 세련되어서 일상용으로 좋아요."},
        {"text": "손잡이가 튼튼하게 제작되어 있어 안심돼요."},
        {"text": "가방 무게가 좀 무겁습니다."},
        {"text": "주머니 위치가 편리해서 자주 쓰는 물건 넣기 좋아요."},
        {"text": "끈 길이 조절이 어려워요."},
        {"text": "색상이 화면과 거의 동일해서 만족스러워요."},
        {"text": "가죽이 부드러워서 촉감이 좋아요."},
        {"text": "지퍼가 잘 걸려서 열다가 힘들었어요."},
        {"text": "여행, 출퇴근 둘 다 쓰기 적당한 사이즈입니다."},
        {"text": "포켓이 많아 물건 정리하기 편하지만, 조금 복잡해요."},
        {"text": "디자인이 깔끔하고 어떤 옷에도 잘 어울립니다."},
        {"text": "어깨끈이 조금 얇아서 장시간 착용하면 불편합니다."},
        {"text": "가방 내부가 생각보다 넓고 수납력이 좋아요."},
        {"text": "마감이 정교하고 전체적으로 퀄리티가 좋습니다."},
        {"text": "배송이 늦어서 조금 아쉬웠습니다."},
        {"text": "가방 색상이 다양한 스타일에 잘 어울려서 만족스러워요."}
    ]

    # JSON 문자열로 변환
    reviews_json_str = json.dumps(preprocessed_reviews, ensure_ascii=False)
    product_name = "샘플 상품"
    product_price = "25000원"

    # 요약 호출
    review_summary = summerizeUsecase.summarize_review(product_name, product_price, reviews_json_str)

    # 터미널에 출력
    print("===== Review Summary =====")
    print(review_summary)
    print("==========================")

