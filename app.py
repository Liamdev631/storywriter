from backend.content import Content
from backend.generators import MainStoryGenerator, NormalGenerator, ChapterGenerator
from backend.models import OpenAIModel
import logging
from sys import stdout

logging.basicConfig(stream=stdout, level=logging.INFO)

# Use OpenAI Davinci model
model = OpenAIModel("gpt-3.5-turbo")
logging.info(f"Using engine {model.engine}")

# Generate the introduction to the story
main_story = Content("main_story")
main_story.description = "A novel about a man named Simon. Every time Simon dies, he is reborn into the same body on the same day in January 1947 with all memory from his most recent lives, however Simon has extreme difficulty remembering past 200 years. Around the start of the story, Simon experiences one of his worst deaths. He gives up trying to control his future because nothing ever repeats himself the way he wants. Simon makes a discovery that reinvigorates him, giving him an objective that will take several lifetimes to successfully complete."
logging.info(f"Generating {main_story.name}")
MainStoryGenerator.generate(main_story, model)
main_story.save()

# Create descriptions of the factions in the world
factions_list = Content("bio/characters")
factions_list.description = "A detailed description of the characters in the novel, the vast majority of which Simon is regrettably unable to reconnect with in most lifetimes. Write one friend for Simon that he is consistantly able to reconnect with."
factions_list.dependencies = [main_story.name]
logging.info(f"Generating {factions_list.name}")
NormalGenerator.generate(factions_list, model)
factions_list.save()

# Create a list of all the chapters in the book
chapter_list = Content("planning/chapters_list")
chapter_list.description = "Write a bullet-point list of the 20 chapters in the novel and for each list the 2 most important events in them."
chapter_list.dependencies = [main_story.name, factions_list.name]
logging.info(f"Generating {chapter_list.name}")
NormalGenerator.generate(chapter_list, model)
chapter_list.save()

# Create every chapter of the book
for i in range(1,11):
	chapter = Content(f"chapters/chapter_{i}")
	chapter.description = f"Write chapter {i} of the novel."
	chapter.dependencies = [main_story.name, factions_list.name, chapter_list.name]
	# Include the previous chapter if one exists
	if i > 1:
		chapter.dependencies.append(f"chapters/chapter_{i-1}")
	logging.info(f"Generating {chapter.name}")
	ChapterGenerator.generate(chapter, model)
	chapter.save()

