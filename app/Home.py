import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator
from openai.error import AuthenticationError, RateLimitError
import pandas as pd
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Name of the website
favicon = Image.open("app/resources/icons/favicon.ico")
st.set_page_config(
    page_title="AI FantasyForge",
    page_icon=favicon,
    layout='wide'
)

st.title('Welcome to AI FantasyForge')

col1, col2 = st.columns(2)
with col1:
    # Subtitle or tagline
    st.subheader('Unleash your Imagination, Power your Storytelling')

    # Introduction about the app
    st.write("""
    **AI FantasyForge** brings the magic of artificial intelligence to your fingertips, making your stories, games, and worlds rich, immersive, and uniquely yours. This is your one-stop-shop for generating custom characters, thrilling quests, unique magic items, and so much more.
    """)

    # About the Interface
    st.header('Simple and Friendly Interface')

    # Content Generation Capabilities
    st.header('Generate Unlimited Content!')
    st.write("""
    - **Characters**: Just provide the basic details and watch as our AI spins out a unique, full-fledged character.
    - **Quests**: Generate compelling quests that keep your players engaged and on their toes.
    - **Magic Items**: Be it a sword with a curse or a potion with unpredictable effects, you can create countless magical items.
    - **And much more!**: Create locations, lore, enemy profiles, non-player characters (NPCs), plot twists and much more!
    """)

    # Invitation to join
    st.header('Try AI FantasyForge Today!')
    st.write("""
    No matter if you're a dungeon master, a writer, or just someone who loves creating fantasy worlds - **AI FantasyForge** is the tool for you!

    Join us in this revolution of AI-driven creativity and take your storytelling to the next level.
    """)
with col2:
    with open('app/users/credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
        
        name, authentication_status, username = authenticator.login('Login', 'main')
        if st.session_state["authentication_status"]:
            authenticator.logout('Logout', 'main')
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.title('Some content')
        elif st.session_state["authentication_status"] == False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] == None:
            st.warning('Please enter your username and password')
