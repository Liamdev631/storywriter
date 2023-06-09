from .generator import Generator
import streamlit as st
from utils import load_list

class WorldGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD World Generator')
        
        editions_list: list[str] = ['5th', '4th', '3rd', '2nd', '1st']
        worlds_list: list[str] = load_list("app/resources/dnd/worlds.csv")
        
        col1, col2 = st.columns(2)
        params = {}
        
        with col1:
            params['edition'] = st.selectbox('Edition', options=editions_list, index=editions_list.index('5th'))
            params['world_type'] = st.selectbox('World Type', options=worlds_list, index=worlds_list.index('Standard'))
        
        with col2:
            params['magic_prevalance'] = st.slider('Magic Prevalance', value=10, min_value=1, max_value=100, step=1)
            params['world_age'] = st.slider('World Age (years)', value=5000, min_value=0, max_value=10000, step=100)
        return params
    
    @staticmethod
    def generate(params: dict[str,str]) -> str:
        prompt: str = "You are an expert DnD Dungeon Master who builds magnificent and diverse worlds for fantasy gaming. Given a rough idea of what they're looking for, you help players dreams meet reality. Your details of the worlds should include the major continents. The development of the world should be consistant with it's age. For example, a young world of several hundred years likely will not contain many great nations but an older world of several thousand years should have advanced enough to contruct massive empires. Make no mention of the game or the party and do not break the 4th wall. You must stick to {edition} edition rules. Your responses must be styled like a historical document, being very dense with information and without much filler. Design a {world_type} world. Civilization and culture first appeared on this world {world_age} years ago. In this world, magic is available to {magic_prevalance}% of the population."
        
        return prompt.format(**params)
        