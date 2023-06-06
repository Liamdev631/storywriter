from langchain import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
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
        system_message_template: str = "You are an expert DnD Dungeon Master who builds magnificent and diverse worlds for fantasy gaming. Given a rough idea of what they're looking for, you help players dreams meet reality. You must stick to {edition} edition rules."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template).format(**params)
        
        human_message_template: str = "Civilization and culture first appeared on this world {world_age} years ago. In this world, magic is available to {magic_prevalance}% of the population."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template).format(**params)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        return chain.run("")
        