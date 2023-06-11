
from abc import abstractmethod

class Generator():
    @abstractmethod
    def load_gui(self) -> None:
        pass
    
    @abstractmethod
    def generate(self) -> None:
        pass