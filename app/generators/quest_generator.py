from langchain import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from .generator import Generator
import streamlit as st
from utils import load_list

class QuestGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD Quest Generator')
        
        difficulty_options = ["Easy", "Normal", "Hard", "Extreme", "Impossible"]
        
        params = {}
        
        params['avg_party_level'] = st.number_input(label='Average Party Level', value=1, min_value=1)
        params['party_size'] = st.number_input(label='Party Size', value=2, min_value=1)
        params['difficulty'] = st.selectbox(label='Difficulty', options=difficulty_options, index=difficulty_options.index('Normal'))
                
        return params
    
    @staticmethod
    def generate(params: dict[str,str]) -> str:
        prompt: str = "You are an expert DnD Dungeon Master who designs unique and exotic quests for your players based on their specifications. Please generate a(n) {difficulty} DnD quest for {party_size} players that is unique and fun. The average level of players in the party is {avg_party_level}"
        
        return prompt.format(**params)
        