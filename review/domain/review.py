from dataclasses import dataclass

"""크롤링한 원본 리뷰"""
@dataclass
class RawReview:
    id: str
    text: str


"""전처리된 리뷰"""
@dataclass
class ProcessedReview:
    id: str
    original_text: str
    cleaned_text: str
    tokens: list[str]
    processed_text: str

    @property
    def word_count(self) -> int:
        """단어 개수"""
        return len(self.tokens)

    @property
    def is_valid(self) -> bool:
        """유효한 리뷰인지 (최소 2단어 이상)"""
        return len(self.tokens) >= 2 and len(self.cleaned_text) >= 5