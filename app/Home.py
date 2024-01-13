import streamlit as st
from PIL import Image

# Name of the website
favicon = Image.open("app/resources/icons/favicon.ico")
st.set_page_config( # type: ignore
    page_title="AI FantasyForge",
    page_icon=favicon,
    layout='wide'
)

st.title('Welcome to AI FantasyForge')

# Subtitle or tagline
st.subheader('Unleash your Imagination, Power your Storytelling')

# Introduction about the app
st.write("""
**AI FantasyForge** brings the magic of artificial intelligence to your fingertips, making your stories, games, and worlds rich, immersive, and uniquely yours. This is your one-stop-shop for generating custom characters, thrilling quests, unique magic items, and so much more.
""")

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
No matter if you're a dungeon master, a writer, or just someone who loves creating fantasy worlds - **AI FantasyForge** is the tool for you! Join us in this revolution of AI-driven creativity and take your storytelling to the next level.
""")

# Instructions
st.write("To get started, select the toolset you want from the side panel and choose your generator!")
    

