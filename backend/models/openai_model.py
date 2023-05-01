from backend.models import Model
import openai
import backoff
import re
from openai.error import RateLimitError

@backoff.on_exception(backoff.expo,
		      RateLimitError,
			  max_time=240)
def get_raw_response(**kwargs):
	return openai.ChatCompletion.create(**kwargs)

class OpenAIModel(Model):
	def get_response(self, prompt_text: str):
		# Set the OpenAI API key if it hasn't already
		if openai.api_key is None:
			with open("api.env", "r") as file:
				content = file.read()
				match = re.search(r"openai-secret:\s+(\S+)", content)
				if match:
					openai.api_key = match.group(1)
				else:
					raise ValueError("API key not found in ./api.env!")

		# Query the OpenAI API for a response

		response = get_raw_response(
			model=self.engine,
			messages=[
				{'role': 'user', 'content': prompt_text}
			],
			max_tokens=1024,
			n=1,
			stop=None,
			temperature=0.8,
		)
		
		# Get the first response and its text
		response_text: str = response['choices'][0]['message']['content'].strip() # type: ignore
		return response_text
