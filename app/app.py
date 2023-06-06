import streamlit as st
st.set_page_config(layout="wide")
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator
from openai.error import AuthenticationError, RateLimitError
import pandas as pd

# Checking if the session state is already defined
if 'params' not in st.session_state:
    # Initializing a new session state
    st.session_state['params'] = {}

st.title('Storywriter')

generator_options = ('None', 'Item', 'Character', 'World', 'Quest')

def on_generator_changed():
    st.session_state['params'] = {}

with st.sidebar:
    st.session_state['selected_generator_name'] = st.selectbox(label="Select your generator.", options=generator_options, index=generator_options.index('None'), on_change=on_generator_changed)
    
    st.session_state['key'] = st.text_input(label='OpenAI API Key', value='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', help="This key is required to access GPT from OpenAI. Ask Liam if he didn't give you one.")

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
        case _:
            return WorldGenerator() # Default
        
if st.session_state['selected_generator_name'] == 'None':
    # Title of the page
    st.title('Welcome to StoryWriter')

    # Subtitle or tagline
    st.subheader('Unleash your Imagination, Power your Storytelling')

    # Introduction about the app
    st.write("""
    **StoryWriter** brings the magic of artificial intelligence to your fingertips, making your stories, games, and worlds rich, immersive, and uniquely yours. This is your one-stop-shop for generating custom characters, thrilling quests, unique magic items, and so much more.
    """)

    # About the Interface
    st.header('Simple and Friendly Interface')
    st.image('url-to-the-app-screenshot')

    # Content Generation Capabilities
    st.header('Generate Unlimited Content!')
    st.write("""
    - **Characters**: Just provide the basic details and watch as our AI spins out a unique, full-fledged character.
    - **Quests**: Generate compelling quests that keep your players engaged and on their toes.
    - **Magic Items**: Be it a sword with a curse or a potion with unpredictable effects, you can create countless magical items.
    - **And much more!**: Create locations, lore, enemy profiles, non-player characters (NPCs), plot twists and much more!
    """)

    # Invitation to join
    st.header('Try StoryWriter Today!')
    st.write("""
    No matter if you're a dungeon master, a writer, or just someone who loves creating fantasy worlds - **StoryWriter** is the tool for you!

    Join us in this revolution of AI-driven creativity and take your storytelling to the next level.
    """)
    st.stop()

# Retrieve the generator instance
selected_generator: Generator = get_generator_by_name(st.session_state['selected_generator_name'])

options_col, result_col = st.columns(2)

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
