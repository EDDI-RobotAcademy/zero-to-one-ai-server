class ReviewPrompts:
    @staticmethod
    def summary(product_name: str, preprocessed_reviews: str) -> str:
        return f"""
        당신은 전자상거래 리뷰 분석 전문가입니다.
        아래는 전처리된 리뷰 데이터이며, **상품 '{product_name}'을 중심으로** 리뷰 내용만 기반해 정확한 JSON을 생성해야 합니다.

        입력 리뷰(전처리 완료):
        {preprocessed_reviews}

        요구 사항:
        1) "summary": 리뷰 전체의 핵심 내용을 2~4문장으로 간결하게 요약
        2) "positive_features": 긍정적인 요소 1~2줄 요약
        3) "negative_features": 반복된 불만 1~2줄 요약, 없으면 "없음"
        4) "keywords": 긍정 키워드 5~6개 추출, 부정 키워드 제외, 중복 제거

        반드시 JSON 스키마에 따라 출력, 추가 문장/설명 없이 순수 JSON 반환:
        {{
          "summary": "요약문장...",
          "positive_features": "긍정 요소 요약...",
          "negative_features": "부정 요소 요약 또는 없음",
          "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
        }}

        제약:
        - 입력 리뷰 외 사실 추가 금지
        - 모든 값은 문자열 또는 배열, null/undefined 금지
        - 출력은 반드시 유효한 JSON
        """