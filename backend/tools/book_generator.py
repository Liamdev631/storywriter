import logging
from pylatex import Document, Package, Command, Section
from pylatex.utils import bold
from datetime import date
from dataclasses import dataclass
from backend.content import Content
from backend.generators import MainStoryGenerator, NormalGenerator, ChapterGenerator
from backend.models import Model

@dataclass
class BookParams:
	title: str = "Title"
	author: str = "Author"
	synopsis: str = "Synopsis"
	num_chapters: int = 10
	page_width: int = 5
	page_height: int = 8
	margin: int = 1


class BookGenerator:
	@staticmethod
	def generate(params: BookParams, model: Model):
		# Generate the synopsis
		synopsis = Content("synopsis")
		synopsis.description = params.synopsis
		logging.info(f"Generating {synopsis.name}")
		MainStoryGenerator.generate(synopsis, model)
		synopsis.save()

		# Extrapolate the synopsis into a list of chapters.
		chapter_list = Content("condensed/chapter_list")
		chapter_list.description = f"Generate a condensed list of the {params.num_chapters} chapters composing your novel and list the 2 or 3 most important events in each chapter. Make the plot interesting and diverse."
		chapter_list.dependencies = [synopsis.name]
		logging.info(f"Generating {chapter_list.name}")
		NormalGenerator.generate(chapter_list, model)
		chapter_list.save()

		# Generate each chapter of the book
		for i in range(1, params.num_chapters+1):
			chapter = Content(f"chapters/chapter_{i}")
			chapter.description = f"Generate chapter {i} of the novel. Do concise and do not include dialog, descriptive language or filler."
			chapter.dependencies = [synopsis.name, chapter_list.name]
			# Include the previous chapters if they exist
			if i > 1: chapter.dependencies.append(f"chapters/chapter_{i-1}")
			if i > 2: chapter.dependencies.append(f"chapters/chapter_{i-2}")
			logging.info(f"Generating {chapter.name}")
			ChapterGenerator.generate(chapter, model)
			chapter.save()

	@staticmethod
	def build(params: BookParams):
		logging.info(f"Generating {params.title}.tex")
		doc = Document(documentclass='book', default_filepath="output/" + params.title)
		
		doc.packages.append(Package('graphicx'))
		doc.packages.append(Package('geometry', options=f"paperwidth={params.page_width}in, paperheight={params.page_height}in, margin={params.margin}in"))
		doc.packages.append(Package('fancyhdr'))
		doc.packages.append(Package('floatpag'))
		
		doc.preamble.append(Command('pagestyle', 'fancy'))
		
		doc.preamble.append(Command('title', params.title))
		doc.preamble.append(Command('author', params.author))
		
		today = date.today()
		month_year = today.strftime("%B %Y")
		doc.preamble.append(Command('date', month_year))
		
		doc.append(Command('maketitle'))

		# Add each chapter
		for i in range(1, params.num_chapters+1):
			content = Content.load(f"chapters/chapter_{i}")
			doc.append(content.text)

		doc.generate_tex()
		logging.info(f"{params.title}.tex saved!")
