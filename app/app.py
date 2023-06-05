import streamlit as st
import os

os.environ['OPENAI_API_KEY'] = st.text_input(label='OpenAI API Key', value=st.session_state['openai_api_key'])

from langchain import OpenAI
from langchain.llms import OpenAI, OpenAIChat
from langchain.llms.base import BaseLLM
import pandas as pd
from generators import Generator, CharacterGenerator

st.set_page_config(layout="wide")

# Checking if the session state is already defined
if 'params' not in st.session_state:
    # Initializing a new session state
    st.session_state['params'] = {}

st.title('Storywriter')

#llm: BaseLLM = OpenAIChat(client=None, model_name='gpt-3.5-turbo')
llm: BaseLLM = OpenAI(client=None, model_name='text-davinci-003', max_tokens=1024)

# Retrieve the generator instance
selected_generator: Generator = CharacterGenerator()

options_col, result_col = st.columns(2)

with options_col:
    # Load the GUI and store the parameters
    params = selected_generator.load_gui()

    # Store the parameters in the session state
    st.session_state['params'] = params

if st.button('Generate'):
    with result_col:
        st.session_state['result'] = selected_generator.generate(llm, params)
        st.markdown(st.session_state['result'], unsafe_allow_html=False)
