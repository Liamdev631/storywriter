import streamlit as st
st.set_page_config(layout="wide")
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator
from openai.error import AuthenticationError, RateLimitError
import pandas as pd
from pages import draw_landing

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
    draw_landing()
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
