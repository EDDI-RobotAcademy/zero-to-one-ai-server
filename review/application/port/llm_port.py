from abc import ABC, abstractmethod


class LLMPort(ABC):
    @abstractmethod
    def summarize(self, prompt: str) -> str:
        pass