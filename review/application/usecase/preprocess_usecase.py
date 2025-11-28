import json
import re
from html import unescape
from typing import Dict, Iterable, List, Sequence

EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010FFFF]", flags=re.UNICODE)
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
REPETITION_PATTERN = re.compile(r"(.)\1{1,}")

class PreprocessUseCase:
    """
    리뷰 텍스트를 정제하고 요약기에 바로 전달할 수 있는 JSON 페이로드를 생성
    - HTML 태그 제거
    - 이모지/특수문자 정리
    - 의미 없는 짧은 문장 필터링 및 중복 제거
    - 문장 단위 분할로 긴 문장 품질 관리
    """

    def __init__(
            self,
            *,
            min_text_length: int = 5,
            min_word_count: int = 2,
            max_sentence_length: int = 180,
            noise_tokens: Sequence[str] | None = None,
    ):
        self.min_text_length = min_text_length
        self.min_word_count = min_word_count
        self.max_sentence_length = max_sentence_length
        self.noise_tokens = noise_tokens or (
            "ㅋㅋ",
            "ㅎㅎ",
            "ㅠㅠ",
            "ㅜㅜ",
            "굿",
            "좋아요",
        )

    def execute(self, raw_reviews: Dict | List[str] | List[Dict[str, str]]) -> Dict:
        texts = list(self._normalize_reviews(raw_reviews))

        cleaned_items: List[Dict[str, str]] = []
        dropped_count = 0

        for idx, text in enumerate(texts, start=1):
            normalized = self._clean_text(text)
            if not self._passes_filters(normalized):
                dropped_count += 1
                continue

            sentences = self._split_sentences(normalized)
            if not sentences:
                dropped_count += 1
                continue

            cleaned_text = " ".join(sentences)
            cleaned_items.append({"id": idx, "text": cleaned_text, "sentences": sentences})

        deduped_items = self._deduplicate(cleaned_items)
        deduplicated_count = len(cleaned_items) - len(deduped_items)

        payload = json.dumps([
            {"text": item["text"]} for item in deduped_items
        ], ensure_ascii=False)

        return {
            "clean_reviews": deduped_items,
            "stats": {
                "input_count": len(texts),
                "dropped_count": dropped_count + deduplicated_count,
                "deduplicated_count": deduplicated_count,
                "kept_count": len(deduped_items),
            },
            "json_payload": payload,
        }

    def _normalize_reviews(self, raw_reviews: Dict | List[str] | List[Dict[str, str]]) -> Iterable[str]:
        if isinstance(raw_reviews, dict):
            return [str(value) for value in raw_reviews.values()]

        if isinstance(raw_reviews, list):
            if not raw_reviews:
                return []

            if isinstance(raw_reviews[0], dict):
                return [str(item.get("text", "")) for item in raw_reviews]

            return [str(item) for item in raw_reviews]

        raise ValueError("리뷰 입력 형식이 올바르지 않습니다. dict 또는 list 형태여야 합니다.")

    def _clean_text(self, text: str) -> str:
        text = unescape(str(text))
        text = HTML_TAG_PATTERN.sub(" ", text)
        text = EMOJI_PATTERN.sub(" ", text)
        text = re.sub(r"[^0-9A-Za-z가-힣 ,.!?~]+", " ", text)
        text = WHITESPACE_PATTERN.sub(" ", text).strip()
        text = self._normalize_repetitions(text)
        return text

    def _passes_filters(self, text: str) -> bool:
        if len(text) < self.min_text_length:
            return False

        words = text.split()
        if len(words) < self.min_word_count:
            return False

        collapsed = text.replace(" ", "")
        if any(pattern.match(collapsed) for pattern in self._noise_patterns()):
            return False

        unique_chars = set(collapsed)
        return len(unique_chars) > 1

    def _noise_patterns(self) -> List[re.Pattern[str]]:
        base_patterns = [
            re.compile(r"^[ㅋㅎㅜㅠ]+$"),
            re.compile(r"^[.!?~]+$"),
        ]
        base_patterns.extend(re.compile(rf"^{re.escape(token)}+$", re.IGNORECASE) for token in self.noise_tokens)
        return base_patterns

    def _normalize_repetitions(self, text: str) -> str:
        text = re.sub(r"([.!?~])\1{1,}", r"\1", text)
        text = REPETITION_PATTERN.sub(r"\1", text)
        text = re.sub(r"(요|여|야|유)(오+)", r"\1", text)
        return text

    def _split_sentences(self, text: str) -> List[str]:
        if not text:
            return []

        raw_sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
        sentences: List[str] = []

        for sentence in raw_sentences:
            normalized = sentence.strip()
            if not normalized:
                continue

            if len(normalized) > self.max_sentence_length:
                sentences.extend(self._split_long_sentence(normalized))
                continue

            sentences.append(normalized)

        return [s for s in sentences if len(s) >= self.min_text_length]

    def _split_long_sentence(self, sentence: str) -> List[str]:
        segments = [segment.strip() for segment in re.split(r",\s*", sentence) if segment.strip()]
        if not segments:
            return self._chunk_sentence(sentence)

        results: List[str] = []
        for segment in segments:
            if len(segment) > self.max_sentence_length:
                results.extend(self._chunk_sentence(segment))
            else:
                results.append(segment)

        return results

    def _chunk_sentence(self, sentence: str) -> List[str]:
        chunks: List[str] = []
        for start in range(0, len(sentence), self.max_sentence_length):
            chunk = sentence[start : start + self.max_sentence_length].strip()
            if chunk:
                chunks.append(chunk)
        return chunks

    def _deduplicate(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        seen = set()
        unique_items = []
        for item in items:
            text = item["text"]
            if text in seen:
                continue
            seen.add(text)
            unique_items.append(item)
        return unique_items