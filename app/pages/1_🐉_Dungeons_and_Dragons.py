import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator, DungeonGenerator
from openai.error import AuthenticationError, RateLimitError
from PIL import Image

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
    #st.session_state['key'] = st.text_input(label='OpenAI API Key', value='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', help="This key is required to access GPT from OpenAI. Ask Liam if he didn't give you one.")
    st.session_state['key'] = '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'


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
    params = selected_generator.load_gui()
    st.session_state['params'] = params

if st.button('Generate'):
    with result_col:
        if st.session_state['key'] != '':
            try:
                llm = ChatOpenAI(client=None, model_name='gpt-3.5-turbo', openai_api_key=st.session_state['key'], temperature=0.9)
                st.session_state['result'] = selected_generator.generate(llm, st.session_state['params'])
                st.markdown(st.session_state['result'], unsafe_allow_html=False)
            except AuthenticationError:
                st.warning('Error authenticating! Check your OpenAI AI key and try again.')
            except RateLimitError:
                st.warning('Rate limit reached. Just wait a minute and try again, because of the key everyone is sharing.')
                
        else:
            st.markdown('You must set the OpenAI API Key!')
