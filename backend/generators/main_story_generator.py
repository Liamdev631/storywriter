from .generator import Generator
from backend.content import Content
from backend.models import Model

class MainStoryGenerator(Generator):
	@staticmethod
	def generate(content: Content, model: Model):
		content.prompt = f"You are an expert novel writer. Expand upon the given description of a story to generate a more interesting plot and add interesting filler material. \n\nDescription: \n\n{content.description}\n\nGenerated Content:"

		content.text = model.get_response(content.prompt)