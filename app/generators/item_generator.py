from langchain import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from .generator import Generator
import streamlit as st
from utils import load_list

class ItemGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD Magical Item Generator')
        
        rarity_list: list[str] = load_list("app/resources/dnd/rarities.csv")
        item_types_list: list[str] = load_list("app/resources/dnd/item_types.csv")
        
        col1, col2 = st.columns(2)
        
        params = {}
        
        with col1:
            params['item_type'] = st.selectbox(label='Item Type', options=item_types_list, index=item_types_list.index('Ring'))
            params['rarity'] = st.selectbox(label='Rarity', options=rarity_list, index=rarity_list.index('Legendary'))
            
        with col2:
            params['is_magic'] = "magic" if st.checkbox(label='Magic?') else "entirely non-magic, entirely physical, completely unspecial"
        return params
    
    @staticmethod
    def generate(llm, params: dict) -> str:
        system_message_template: str = "You are an expert DnD Dungeon Master who designs unique and mysterious items for your players based on their specifications."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
        
        human_message_template: str = "Please generate a {is_magic} {item_type} with {rarity} rarity that is unique and fun for DnD players."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        return chain.run(**params)
        