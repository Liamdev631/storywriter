from langchain import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

from .generator import Generator
import streamlit as st
from utils import load_list

class DungeonGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD Dungeon Generator')
        
        params = {}
        
        dungeon_types_list: list[str] = load_list("app/resources/dnd/dungeons.csv")
        
        params['dungeon_type'] = st.selectbox(label='Dungeon Type', options=dungeon_types_list)
        params['num_encounters'] = st.number_input(label='Number of Encounters', min_value=1, value=1)
        
        return params
    
    @staticmethod
    def generate(llm, params: dict) -> str:
        system_message_template: str = "You are an expert DnD Dungeon Master who designs unique and mysterious dungeons for your players based on specifications."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
        
        human_message_template: str = "Please generate a unique and fun {dungeon_type} dungeon for a party of DnD players. The dungeon must include {num_encounters} encounters."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        return chain.run(**params)
        