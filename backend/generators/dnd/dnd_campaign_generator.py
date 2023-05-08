from ..generator import Generator
from backend.content import Content
from backend.models import Model
from backend.generators.dnd import DnDCampaignSettings

class DnDCampaignGenerator(Generator):
	@staticmethod
	def generate(content: Content, model: Model, dnd_settings: DnDCampaignSettings):
		content.prompt = f"You are Brennan Lee Mulligan, an expert Dungeon Master. Design a D&D campaign for {dnd_settings.num_players} and write a 500 word synopsis that summarizes it. Incorporate the following elements in your design: {content.description}\n\n"

		content.text = model.get_response(content.prompt)