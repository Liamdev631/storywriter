from .generator import Generator
from backend.content import Content
from backend.models import Model

class ChapterGenerator(Generator):
	@staticmethod
	def generate(content: Content, model: Model, word_count_target=1000):
		# Pull all the dependency text in one string
		dependency_texts: str = ""
		for dep_name in content.dependencies:
			dep = Content.load(dep_name)
			dependency_texts += f'\n\n{dep.name}:\n{dep.text}'

		# Stitch everything together in the prompt
		content.prompt = f"You are an expert novelist. Generate a well-written chapter. MUST contain at least {word_count_target} words, and you MUST place the title of the chapter in a latex /chapter{{}} command. Incorporate the following chapter description and dependencies info: \n\nDependencies: {dependency_texts}\n\n Description: \n{content.description}\n\n Generated Chapter:\n"

		# Trim the response and update the content
		response = model.get_response(content.prompt).strip()
		content.text = response
