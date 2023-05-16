from langchain.prompts import PromptTemplate
from generators import AbstractPromptGen

class Campaign(AbstractPromptGen):
	@staticmethod
	def generate(args: dict = {'edition': '5th', 'num_players': 1}) -> PromptTemplate:
		template = """
		I want you to act as a Dungeon Master for an edition {edition} DnD campaign for {num_players} players.
		Please write the synopsis of the campaign. Be specific in including main enemies, factions and locations. Must include enough information to get the players interested in playing the campaign at first glance.
		"""
		return PromptTemplate.from_template(template).format(**args)