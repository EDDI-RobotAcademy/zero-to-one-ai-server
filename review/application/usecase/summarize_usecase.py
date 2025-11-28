import logging
import json

from review.application.port.llm_port import LLMPort
from review.review_summarize_prompt import ReviewPrompts

logger = logging.getLogger(__name__)

class SummarizeUseCase:
    def __init__(self, llm_port: LLMPort):
        self.llm_port = llm_port

    def summarize_review(self, product_name: str, preprocessed_reviews: str) -> dict:

        # 프롬프트 생성
        prompt = ReviewPrompts.summary(product_name, preprocessed_reviews)

        # LLM 호출 (Adapter에서 재시도 + 실패 시 빈 JSON 문자열 반환)
        llm_response_str = self.llm_port.summarize(prompt)  # LLM에서 받은 원본 문자열
        summary_data = json.loads(llm_response_str)  # JSON → dict로 변환된 요약 데이터

        return summary_data
