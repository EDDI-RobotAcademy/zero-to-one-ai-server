from konlpy.tag import Okt
from application.port.preprocessor_port import TokenizerPort


class KoNLPyTokenizer(TokenizerPort):
    """KoNLPy를 사용한 형태소 분석"""

    def __init__(self):
        self.okt = Okt()

        # 불용어 리스트
        self.stopwords = {
            '이', '그', '저', '것', '수', '등', '들', '및',
            '요', '네요', '어요', '습니다', '입니다',
            '있다', '하다', '되다', '이다'
        }

    def tokenize(self, text: str) -> list[str]:
        """형태소 분석 (명사, 형용사, 동사만 추출)"""
        tokens = self.okt.pos(text, stem=True)

        # 명사, 형용사, 동사만 추출
        meaningful_tokens = [
            word for word, pos in tokens
            if pos in ['Noun', 'Adjective', 'Verb']
        ]

        return meaningful_tokens

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """불용어 제거 (1글자 단어도 제거)"""
        return [
            token for token in tokens
            if token not in self.stopwords and len(token) > 1
        ]