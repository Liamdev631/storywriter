from widgets import OpenAIGenerationWidget
from generators import Generator
import streamlit as st
from utils import load_list

class QuestGenerator(Generator):
    def __init__(self):
        options_col, result_col = st.columns(2) 

        with options_col:
            self.load_gui()

        with result_col:
            if st.button('Generate'):
                self.generate()
                
    def load_gui(self) -> None:
        st.title('DnD Quest Generator')
        
        difficulty_options = ["Easy", "Normal", "Hard", "Extreme", "Impossible"]
        
        params = {}
        
        params['avg_party_level'] = st.number_input(label='Average Party Level', value=1, min_value=1)
        params['party_size'] = st.number_input(label='Party Size', value=2, min_value=1)
        params['difficulty'] = st.selectbox(label='Difficulty', options=difficulty_options, index=difficulty_options.index('Normal'))
                
        st.session_state['params'] = params
        
    def generate(self) -> None:
        prompt: str = "You are an expert DnD Dungeon Master who designs unique and exotic quests for your players based on their specifications. Please generate a(n) {difficulty} DnD quest for {party_size} players that is unique and fun. The average level of players in the party is {avg_party_level}. Quests may include individual encounters, dungeons, and other events in multiple locations. Please include secret interactions, shortcuts or special loot that might make the quest more interesting."
        
        openai_widget = OpenAIGenerationWidget(self, prompt.format(**st.session_state['params']))
        