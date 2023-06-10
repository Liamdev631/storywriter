import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = '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'
from langchain.chat_models import ChatOpenAI
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator, DungeonGenerator
from PIL import Image
import openai
from openai.error import AuthenticationError, RateLimitError

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
    params = selected_generator.load_gui()
    st.session_state['params'] = params

if st.button('Generate', type='primary'):
    with result_col:
        wait_message = st.markdown("----Generating! Please wait 15-30 seconds.----")
        try:
            combined = []
            result_box = st.empty()
            prompt = selected_generator.generate(st.session_state['params'])
            result = openai.ChatCompletion.create(model='gpt-3.5-turbo', temperature=1.0, stream=True, messages=[{'role': 'user', 'content': prompt}])
            for response_chunk in result:
                response_text = response_chunk['choices'][0]['delta'] # type: ignore
                answer = response_text.get('content', '')
                combined.append(answer) # type: ignore
                result_box.markdown(''.join(combined), unsafe_allow_html=False)
            wait_message.empty()
        except AuthenticationError as e:
            if e.code == 401:
                st.warning("Invalid Authentication. Ensure the correct API key and requesting organization are being used.")
                st.warning("Incorrect API key provided. Ensure the API key used is correct, clear your browser cache, or generate a new one.")
                st.warning("You must be a member of an organization to use the API. Contact us to get added to a new organization or ask your organization manager to invite you to an organization.")
            elif e.code == 429:
                st.warning("Rate limit reached for requests. Pace your requests. Read the Rate limit guide.")
                st.warning("You exceeded your current quota, please check your plan and billing details. Apply for a quota increase.")
                st.warning("The engine is currently overloaded, please try again later. Please retry your requests after a brief wait.")
            elif e.code == 500:
                st.warning("The server had an error while processing your request. Retry your request after a brief wait and contact us if the issue persists. Check the status page.")
        except RateLimitError:
            st.warning('Rate limit reached. Just wait a minute and try again, because of the key everyone is sharing.')
