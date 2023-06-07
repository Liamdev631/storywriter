from langchain import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from .generator import Generator
import streamlit as st
from utils import load_list, get_index

class QuestGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD Quest Generator')
        
        editions_list: list[str] = load_list("app/resources/dnd/editions.csv")
        
        params = {}
        
        params['edition'] = st.selectbox('Edition', options=editions_list, key='edition', index=get_index(editions_list, st.session_state['params'].get('edition', None)))
        
        
        return params
    
    @staticmethod
    def generate(llm, params: dict) -> str:
        system_message_template: str = "You are an expert DnD Dungeon Master who designs unique and exotic quests for your players based on their specifications."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
        
        human_message_template: str = "Please generate a quest for {edition} edition DnD that is unique and fun for DnD players."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        return chain.run(**params)
        