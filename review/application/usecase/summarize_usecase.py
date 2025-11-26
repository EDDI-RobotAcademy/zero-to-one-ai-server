import logging
from review.application.port.llm_port import LLMPort
from openai import APIError
from review.review_summarize_prompt import ReviewPrompts

logger = logging.getLogger(__name__)

class SummarizeUseCase:
    def __init__(self, llm_port: LLMPort):
        self.llm_port = llm_port

    def summarize_review(self, product_name: str, product_price: str, preprocessed_reviews: str) -> str:
        # 입력 검증
        if not product_name.strip():
            raise ValueError("상품명이 비어있습니다")
        if not product_price.strip():
            raise ValueError("상품 가격이 비어있습니다")
        if not preprocessed_reviews.strip():
            raise ValueError("리뷰 데이터가 비어있습니다")

        logger.info(f"리뷰 요약 시작: 상품명={product_name}, 가격={product_price}")

        # 프롬프트 생성
        prompt = ReviewPrompts.summary(product_name, product_price, preprocessed_reviews)

        # LLM 호출 (Adapter에서 재시도 + 실패 시 빈 JSON 문자열 반환)
        result_str = self.llm_port.summarize(prompt)

        logger.info(f"리뷰 요약 완료: 상품명={product_name}, 가격={product_price}")
        return result_str
