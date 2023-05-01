import abc
from backend.content import Content

class Generator():
	__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def generate(self, content: Content) -> None:
		pass