from abc import abstractmethod
from langchain.llms.base import BaseLLM

class Generator():
    @staticmethod
    @abstractmethod
    def load_gui():
        pass
    
    @staticmethod
    @abstractmethod
    def generate(llm: BaseLLM,  params: dict) -> str:
        pass