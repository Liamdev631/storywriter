from .generator import Generator
from backend.content import Content
from backend.models import Model

class NormalGenerator(Generator):
	@staticmethod
	def generate(content: Content, model: Model):
		# Pull all the dependency text in one string
		dependency_texts: str = ""
		for dep_name in content.dependencies:
			dep = Content.load(dep_name)
			dependency_texts += f'\n\n{dep.name}:\n{dep.text}'

		# Stitch everything together in the prompt
		content.prompt = f"You are an expert novelist. Generate well-written text from the following Description and Dependencies info: \n\nDependencies:\n {dependency_texts} \n\nDescription: \n{content.description}\n\nGenerated Content:\n"

		# Trim the response and update the content
		response = model.get_response(content.prompt).strip()
		content.text = response