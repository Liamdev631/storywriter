import streamlit as st
from PIL import Image
from auth0_component import login_button

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

    st.write('If you encounter an error, or have suggestions for our team, please shoot us a message. We treat these with the highest priority!')
    st.markdown('<a href="mailto:aistoryforgeapp@gmail.com">Contact us!</a>', unsafe_allow_html=True)

    st.write("Consider supporting server costs and GPT access by donating to our Patreon!")
    link = '<a href="https://www.patreon.com/bePatron?u=94804852" data-patreon-widget-type="become-patron-button">Become a Patron!</a><script async src="https://c6.patreon.com/becomePatronButton.bundle.js"></script>'
    st.markdown(link, unsafe_allow_html=True)

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
    
    
with col2:
    clientId = "z2CFGipjhdeVATUTawXyp6eTJfHeXXB1"
    domain = "dev-vy2zhuaw3evkpb0k.us.auth0.com"
    
    user_info = login_button(clientId, domain = domain)
    st.write(user_info)
