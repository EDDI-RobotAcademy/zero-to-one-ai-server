import logging
import time
from review.application.port.llm_port import LLMPort
from openai import APIError

logger = logging.getLogger(__name__)


class LLMAdapter(LLMPort):

    def __init__(self, client, max_retries: int = 2):
        """
        max_retries: LLM 호출 실패 시 최대 재시도 횟수
        """
        self.client = client
        self.max_retries = max_retries

    def summarize(self, prompt: str) -> str:
        for attempt in range(self.max_retries + 1):
            try:
                result = self.client.call_openai(prompt)
                logger.debug(f"LLM 호출 성공 (attempt {attempt})")
                return result
            except APIError as e:
                if attempt < self.max_retries:
                    wait_time = 2 ** (attempt + 1)
                    logger.warning(f"LLM 호출 실패, {wait_time}초 후 재시도 {attempt + 1}/{self.max_retries}: {str(e)}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"LLM 호출 최종 실패: {str(e)}")
                    # 안전하게 빈 JSON 문자열 반환
                    return '{"summary": "", "positive_features": "", "negative_features": "", "keywords": []}'
            except Exception as e:
                logger.error(f"예상치 못한 오류 발생: {type(e).__name__} - {str(e)}")
                return '{"summary": "", "positive_features": "", "negative_features": "", "keywords": []}'