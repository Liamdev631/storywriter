from langchain import PromptTemplate
from .generator import Generator
import streamlit as st

class WorldGenerator(Generator):
    @staticmethod
    def load_gui():
        params = {}
        params['edition'] = st.selectbox('Edition', ('5th', '4th', '3rd', '2nd', '1st'))
        params['magic_prevalance'] = st.slider('Magic Prevalance', value=10, min_value=1, max_value=100, step=1)
        params['world_age'] = st.slider('World Age (years)', value=5000, min_value=0, max_value=10000, step=100)
        return params
    
    @staticmethod
    def generate(llm, params: dict) -> str:
        template: str = "You are a DnD Dungeon Master. Design a {world_age} year old world for a {edition} edition campaign. In this world, magic is available to {magic_prevalance}% of the population."
        prompt: str = PromptTemplate.from_template(template=template).format(**params)
        return llm(messages=[prompt]).content
        