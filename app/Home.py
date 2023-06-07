import streamlit as st
st.set_page_config(layout="wide")
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM
from generators import Generator, CharacterGenerator, WorldGenerator, ItemGenerator, QuestGenerator
from openai.error import AuthenticationError, RateLimitError
import pandas as pd

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