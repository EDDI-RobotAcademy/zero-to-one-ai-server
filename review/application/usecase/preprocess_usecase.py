from domain.review import RawReview, ProcessedReview
from application.port.preprocessor_port import TextCleanerPort, TokenizerPort


# 리뷰 전처리 UseCase
class PreprocessUseCase:

    def __init__(
            self,
            text_cleaner: TextCleanerPort,
            tokenizer: TokenizerPort
    ):
        self.text_cleaner = text_cleaner
        self.tokenizer = tokenizer

# 리뷰 전처리 실행
    def execute(self, raw_reviews: list[RawReview]) -> list[ProcessedReview]:
        processed_reviews = []

        for raw_review in raw_reviews:
            try:
                processed = self._process_single(raw_review)

                # 유효성 검증
                if processed.is_valid:
                    processed_reviews.append(processed)
                else:
                    print(f"리뷰 {raw_review.id} 제외: 너무 짧음")

            except Exception as e:
                print(f"fail to 리뷰 {raw_review.id} 전처리: {e}")
                continue

        return processed_reviews

    def _process_single(self, raw_review: RawReview) -> ProcessedReview:
        # 텍스트 정제
        cleaned = self.text_cleaner.clean(raw_review.text)

        tokens = self.tokenizer.tokenize(cleaned)

        filtered_tokens = self.tokenizer.remove_stopwords(tokens)

        return ProcessedReview(
            id=raw_review.id,
            original_text=raw_review.text,
            cleaned_text=cleaned,
            tokens=filtered_tokens,
            processed_text=' '.join(filtered_tokens)
        )

    def get_statistics(self, processed_reviews: list[ProcessedReview]) -> dict:
        if not processed_reviews:
            return {"total_reviews": 0}

        return {
            "total_reviews": len(processed_reviews),
            "avg_word_count": sum(r.word_count for r in processed_reviews) / len(processed_reviews),
            "min_word_count": min(r.word_count for r in processed_reviews),
            "max_word_count": max(r.word_count for r in processed_reviews)
        }
