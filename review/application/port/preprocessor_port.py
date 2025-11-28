from abc import ABC, abstractmethod

"""텍스트 정제 인터페이스"""
class TextCleanerPort(ABC):

    """HTML 태그 제거 및 텍스트 정제"""
    @abstractmethod
    def clean(self, text: str) -> str:
        pass


class TokenizerPort(ABC):

    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        pass

    """불용어 제거"""
    @abstractmethod
    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        pass