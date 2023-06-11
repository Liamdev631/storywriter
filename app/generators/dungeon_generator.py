from widgets import OpenAIGenerationWidget
from generators import Generator
import streamlit as st
from utils import load_list

class DungeonGenerator(Generator):
    def __init__(self):
        options_col, result_col = st.columns(2) 

        with options_col:
            self.load_gui()

        with result_col:
            if st.button('Generate'):
                self.generate()

    
    def load_gui(self):
        st.title('DnD Dungeon Generator')
        
        dungeon_types_list: list[str] = load_list("app/resources/dnd/dungeons.csv")
        difficulty_options = ["Easy", "Normal", "Hard", "Extreme", "Impossible"]
        
        params = {}
        
        params['dungeon_type'] = st.selectbox(label='Dungeon Type', options=dungeon_types_list)
        params['num_encounters'] = st.number_input(label='Number of Encounters', min_value=1, value=1)
        params['avg_party_level'] = st.number_input(label='Average Party Level', value=1, min_value=1)
        params['party_size'] = st.number_input(label='Party Size', value=2, min_value=1)
        params['difficulty'] = st.selectbox(label='Difficulty', options=difficulty_options, index=difficulty_options.index('Normal'))
        
        st.session_state['params'] = params
    
    def generate(self):
        prompt: str = "You are an expert DnD Dungeon Master. Design a unique and mysterious {dungeon_type} dungeon for {party_size} players with an average level of {avg_party_level} with {difficulty} difficulty. The dungeon must include {num_encounters} encounter(s). For each encounter, list one or two special interactions the players might take advantage of. You may also include special interactions or hidden treasures/areas within the dungeon outside of encounters, which may provide the party with shortcuts, advantages, or special loot."
        
        params = st.session_state['params']
        openai_widget = OpenAIGenerationWidget(self, prompt.format(**params))
        
