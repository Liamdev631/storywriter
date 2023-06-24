import streamlit as st
from generators import CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator, DungeonGenerator
from PIL import Image

# Name of the website
favicon = Image.open("app/resources/icons/favicon.ico")
st.set_page_config( # type: ignore
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
    st.session_state['selected_generator_name'] = st.selectbox(label="Generator", options=generator_options, index=generator_options.index('Dungeon'), on_change=on_generator_changed)

def get_generator_by_name(generator_name: str) -> object:
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
selected_generator = get_generator_by_name(st.session_state['selected_generator_name'])
