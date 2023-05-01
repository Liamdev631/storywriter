from dataclasses import dataclass, asdict, field
import json
import os

@dataclass
class Content:
	name: str = ""
	description: str = ""
	dependencies: list[str] = field(default_factory=list)
	text: str = ""
	prompt: str = ""

	def save(self) -> None:
		file_path = "content/" + self.name + ".json"
		file_path = file_path.replace(" ", "_").lower()
		os.makedirs(os.path.dirname(file_path), exist_ok=True)
		with open(file_path, 'w') as json_file:
			json.dump(asdict(self), json_file)

	@staticmethod
	def load(file_path: str) -> 'Content':
		file_path = "content/" + file_path + ".json"
		file_path = file_path.replace(" ", "_").lower()
		with open(file_path, 'r') as json_file:
			content_data = json.load(json_file)
		return Content(**content_data)
