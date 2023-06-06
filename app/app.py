import streamlit as st
import os

st.set_page_config(layout="wide")

st.session_state['key'] = st.text_input(label='OpenAI API Key', value='')

from langchain import OpenAI
from langchain.llms import OpenAI, OpenAIChat
from langchain.llms.base import BaseLLM
import pandas as pd
from generators import Generator, CharacterGenerator
from openai.error import AuthenticationError

# Checking if the session state is already defined
if 'params' not in st.session_state:
    # Initializing a new session state
    st.session_state['params'] = {}

st.title('Storywriter')

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
        if st.session_state['key'] != '':
            try:
                #llm: BaseLLM = OpenAIChat(client=None, model_name='gpt-3.5-turbo')
                llm: BaseLLM = OpenAI(client=None, model_name='text-davinci-003', max_tokens=1024, openai_api_key=st.session_state['key'])
                st.session_state['result'] = selected_generator.generate(llm, params)
                st.markdown(st.session_state['result'], unsafe_allow_html=False)
            except AuthenticationError:
                st.markdown('Error authenticating! Check your OpenAI AI key and try again.')
                
        else:
            st.markdown('You must set the OpenAI API Key!')