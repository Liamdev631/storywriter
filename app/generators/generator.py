from abc import abstractmethod

class Generator():
    @staticmethod
    @abstractmethod
    def load_gui():
        pass
    
    @staticmethod
    @abstractmethod
    def generate(params: dict[str,str]) -> str:
        pass