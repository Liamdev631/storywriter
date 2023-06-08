from langchain import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from .generator import Generator
import streamlit as st
from utils import load_list
import openai

class ItemGenerator(Generator):
    @staticmethod
    def load_gui():
        st.title('DnD Magical Item Generator')
        
        races_list: list[str] = load_list("app/resources/dnd/races.csv")
        alignment_list: list[str] = load_list("app/resources/dnd/alignments.csv")
        rarity_list: list[str] = load_list("app/resources/dnd/rarities.csv")
        item_types_list: list[str] = load_list("app/resources/dnd/item_types.csv")
        class_list: list[str] = load_list("app/resources/dnd/classes.csv")
        powers_list: list[str] = load_list("app/resources/dnd/powers.csv")
        affinities_list: list[str] = load_list("app/resources/dnd/affinities.csv")
        
        col1, col2 = st.columns(2)
        
        params = {}
        
        with col1:
            params['item_type'] = st.selectbox(label='Item Type', options=item_types_list, index=item_types_list.index('Ring'))
            params['rarity'] = st.selectbox(label='Rarity', options=rarity_list, index=rarity_list.index('Legendary'))
            params['alignment'] = st.selectbox(label='Alignment', options=alignment_list, index=alignment_list.index(''))
            params['origin_race'] = st.selectbox(label='Origin', options=races_list, index=races_list.index(''))
            params['target_class'] = st.selectbox(label='Target Class', options=class_list, index=class_list.index(''))
            
        with col2:
            params['power1'] = st.selectbox(label='Power 1', options=powers_list, index=powers_list.index(''))
            params['power2'] = st.selectbox(label='Power 2', options=powers_list, index=powers_list.index(''))
            params['affinity1'] = st.selectbox(label='Affinity 1', options=affinities_list, index=affinities_list.index(''))
            params['affinity2'] = st.selectbox(label='Affinity 2', options=affinities_list, index=affinities_list.index(''))
            params['is_magic'] = "magic" if st.checkbox(label='Magic?') else "entirely non-magic, entirely physical"
            params['has_drawbacks'] = "magic" if st.checkbox(label='Drawbacks?') else "entirely non-magic, entirely physical"
        return params
    
    @staticmethod
    def generate(llm, params: dict) -> str:
        system_message_template: str = "You are an expert DnD Dungeon Master who designs unique and mysterious items for your players based on their specifications."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
        
        human_message_template: str = "Please generate a {is_magic} {item_type} with {rarity} rarity that is unique and fun for DnD players."
        if params['power1'] != '':
            human_message_template += " This item has {power1} power."
        if params['power2'] != '':
            human_message_template += " This item has {power2} power."
        if params['affinity1'] != '':
            human_message_template += " This item has {affinity1} affinity."
        if params['affinity2'] != '':
            human_message_template += " This item has {affinity2} affinity."
        if params['target_class'] != '':
            human_message_template += " This item is designed to be useful to players of the {target_class} class."
        if params['origin_race'] != '':
            human_message_template += " This item was created by the {origin_race} race."
        if params['alignment'] != '':
            human_message_template += " This item is must effective when used by one with {alignment} alignment."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        return chain.run(**params)
        