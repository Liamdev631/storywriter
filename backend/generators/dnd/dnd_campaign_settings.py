from dataclasses import dataclass

@dataclass
class DnDCampaignSettings:
	num_players: int = 4
	location: str = ""
