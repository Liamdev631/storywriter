from abc import abstractmethod
from dataclasses import dataclass

@dataclass
class Model():
	engine: str

	@abstractmethod
	def get_response(self, prompt_text: str) -> str:
		pass
