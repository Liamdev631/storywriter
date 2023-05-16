
from abc import ABC, abstractstaticmethod

class AbstractPromptGen(ABC):
    @abstractstaticmethod
    def generate() -> PromptTemplate:
        return "@abstractstaticmethod called!"