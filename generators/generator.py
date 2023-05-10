
from abc import ABC, abstractstaticmethod

class AbstractPromptGen(ABC):
    @abstractstaticmethod
    def generate() -> str:
        return "@abstractstaticmethod called!"