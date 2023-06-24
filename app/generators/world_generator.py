from widgets import OpenAIGenerationWidget
from utils import load_list 
import streamlit as st

class WorldGenerator():
    def __init__(self):
        options_col, result_col = st.columns(2) 

        with options_col:
            self.load_gui()

        with result_col:
            if st.button('Generate'):
                self.generate()
                
    def load_gui(self) -> None:
        st.title('DnD World Generator')
        
        worlds_list: list[str] = load_list("app/resources/dnd/worlds.csv")
        
        col1, col2 = st.columns(2)
        params = {}
        
        with col1:
            params['world_type'] = st.selectbox('World Type', options=worlds_list, index=worlds_list.index('Standard'))
        
        with col2:
            params['magic_prevalance'] = st.slider('Magic Prevalance', value=10, min_value=1, max_value=100, step=1)
            params['world_age'] = st.slider('World Age (years)', value=5000, min_value=0, max_value=10000, step=100)
        
        st.session_state['params'] = params
    
    def generate(self) -> None:
        prompt: str = "You are an expert DnD Dungeon Master who builds magnificent and diverse worlds for fantasy gaming. Given a rough idea of what they're looking for, you help players dreams meet reality. Your details of the worlds should include the major continents. The development of the world should be consistant with it's age. For example, a young world of several hundred years likely will not contain many great nations but an older world of several thousand years should have advanced enough to contruct massive empires. Make no mention of the game or the party and do not break the 4th wall. Your responses must be styled like a historical document, being very dense with information and without much filler. Design a {world_type} world. Civilization and culture first appeared on this world {world_age} years ago. In this world, magic is available to {magic_prevalance}% of the population."
        
        params = st.session_state['params']
        prompt = prompt.format(**params)
        openai_widget = OpenAIGenerationWidget(prompt)
        