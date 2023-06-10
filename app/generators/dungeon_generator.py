from .generator import Generator
import streamlit as st
from utils import load_list

class DungeonGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD Dungeon Generator')
        
        params = {}
        
        dungeon_types_list: list[str] = load_list("app/resources/dnd/dungeons.csv")
        difficulty_options = ["Easy", "Normal", "Hard", "Extreme", "Impossible"]
        
        params['dungeon_type'] = st.selectbox(label='Dungeon Type', options=dungeon_types_list)
        params['num_encounters'] = st.number_input(label='Number of Encounters', min_value=1, value=1)
        params['avg_party_level'] = st.number_input(label='Average Party Level', value=1, min_value=1)
        params['party_size'] = st.number_input(label='Party Size', value=2, min_value=1)
        params['difficulty'] = st.selectbox(label='Difficulty', options=difficulty_options, index=difficulty_options.index('Normal'))
        
        st.session_state['params'] = params
    
    @staticmethod
    def generate(params: dict[str,str]) -> str:
        prompt: str = "You are an expert DnD Dungeon Master. Design a unique and mysterious {dungeon_type} dungeon for {party_size} players with an average level of {avg_party_level} with {difficulty} difficulty. The dungeon must include {num_encounters} encounters."
        
        return prompt.format(**params)
        