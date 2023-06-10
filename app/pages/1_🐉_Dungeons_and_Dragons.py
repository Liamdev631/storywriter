import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = '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'
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator, DungeonGenerator
from PIL import Image
from widgets import OpenAIGenerationWidget

# Name of the website
favicon = Image.open("app/resources/icons/favicon.ico")
st.set_page_config(
        page_title="DnD - AI FantasyForge",
        page_icon=favicon,
        layout='wide'
)

subpage_options = ('About', 'Generators')
generator_options = ('Character', 'Dungeon', 'Item', 'Quest', 'World')

def on_generator_changed():
    st.session_state['params'] = {}

with st.sidebar:
    st.markdown('Select a generator below to get started!')
    st.session_state['selected_generator_name'] = st.selectbox(label="Generator", options=generator_options, index=generator_options.index('Item'), on_change=on_generator_changed)

def get_generator_by_name(generator_name: str) -> Generator:
    match generator_name:
        case "World":
            return WorldGenerator()
        case "Character":
            return CharacterGenerator()
        case "Item":
            return ItemGenerator()
        case "Quest":
            return QuestGenerator()
        case 'Dungeon':
            return DungeonGenerator()
        case _:
            return WorldGenerator()

# Retrieve the generator instance
selected_generator: Generator = get_generator_by_name(st.session_state['selected_generator_name'])

options_col, result_col = st.columns(2) 

if selected_generator == None:
    st.stop()

with options_col:
    # Load the GUI and store the parameters
    selected_generator.load_gui()

with result_col:
    generation_widget = OpenAIGenerationWidget(selected_generator)
