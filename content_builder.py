
import json
from pathlib import Path
from langchain.llms.openai import OpenAI
from langchain.prompts.loading import load_prompt

def generate_content_from_prompt(prompt: str, content_name: str, num_trials: int = 1) -> None:
	llm = OpenAI(model_name='text-davinci-003', client=None, n=num_trials, best_of=num_trials)
	llm_response = llm(prompt)
	content = {'prompt': prompt, 'text': llm_response}
 
	out_path = Path(content_name)
	out_path.parent.mkdir(parents=True, exist_ok=True)
	out_path.touch(exist_ok=True)
	with out_path.open(mode='w+') as f:
		json.dump(content, f, indent=0)