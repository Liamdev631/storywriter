import logging
from sys import stdout
from backend.content import Content
from backend.models import OpenAIModel
from backend.tools import BookGenerator, BookParams

logging.basicConfig(stream=stdout, level=logging.INFO)

model = OpenAIModel("gpt-3.5-turbo")
logging.info(f"Using engine {model.engine}")

book_params = BookParams(
    author="Liam Bury",
    title="Beauty and the Alien",
    synopsis="A children's book of beauty and the beast, where the beast is Stitch from Lilo and Stitch.",
    num_chapters=10
)

BookGenerator.generate(book_params, model)
BookGenerator.build(book_params)

logging.info("Exiting...")
