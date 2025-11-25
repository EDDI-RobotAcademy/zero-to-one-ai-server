from bs4 import BeautifulSoup
import re
from application.port.preprocessor_port import TextCleanerPort

class BeautifulSoupTextCleaner(TextCleanerPort):

    def clean(self, text: str) -> str:
        # HTML 태그 제거
        text = self._remove_html_tags(text)

        # 이모지 제거
        text = self._remove_emojis(text)

        # 특수 문자 정제
        text = self._clean_special_chars(text)

        # 반복 문자 처리
        text = self._normalize_repeats(text)

        # 공백 제거
        text = self._normalize_whitespace(text)

        return text

    def _remove_html_tags(self, text: str) -> str:
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()

    def _remove_emojis(self, text: str) -> str:
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # 얼굴
            "\U0001F300-\U0001F5FF"  # 기호
            "\U0001F680-\U0001F6FF"  # 교통
            "\U0001F1E0-\U0001F1FF"  # 깃발
            "\u2600-\u26FF"  # 기타
            "\u2700-\u27BF"
            "]+", flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)

    # 특수 문자 정제 후 한글, 영문, 숫자, 기본 문장부호만 남김
    def _clean_special_chars(self, text: str) -> str:
        text = re.sub(r'[^\w\s\.,!?ㄱ-ㅎㅏ-ㅣ가-힣]', '', text)
        return text

    # 반복 문자 처리 : '좋아요오오오' -> '좋아요'
    def _normalize_repeats(self, text: str) -> str:
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)
        return text

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
