from langchain.prompts import PromptTemplate
from generators import AbstractPromptGen

class Character(AbstractPromptGen):
	@staticmethod
	def generate(args: dict = {'edition': '5th', 'num_players': 1}) -> str:
		template = """
		I want you to act as a Dungeon Master for an edition {edition} DnD campaign for {num_players} players.
		Please generate a unique and enjoyable character for one of the party's players, complete with a detailed bio with backstory. Write approximately 500 words about this character. Format all information on this character in an organized json file.
		"""
		return PromptTemplate.from_template(template).format(**args)