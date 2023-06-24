from widgets import OpenAIGenerationWidget
from utils import load_list
import streamlit as st

class ItemGenerator():
    def __init__(self):
        options_col, result_col = st.columns(2) 

        with options_col:
            self.load_gui()

        with result_col:
            if st.button('Generate'):
                self.generate()
                
    def load_gui(self):
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
            params['is_magic'] = st.checkbox(label='Magic?', value=True) 
            params['has_drawbacks'] = st.checkbox(label='Drawbacks?', value=False)
        
        st.session_state['params'] = params
    
    def generate(self):
        params: dict[str,str] = st.session_state['params']
        
        prompt: str = "You are an expert DnD Dungeon Master who designs unique items for your players based on their specifications. Please generate a {item_type} with {rarity} rarity that is unique and fun for DnD players."
        if params['is_magic']:
            prompt += " The item has magical properties."
        else:
            prompt += " The item is entirely non-magical and has no special abilities. It's strength comes from its physical properties."
        if params['has_drawbacks']:
            prompt += " The item has drawbacks that afflict the user when used."
        else:
            prompt += " The item has NO drawbacks that might afflict the user when used."
        if params['power1'] != '':
            prompt += " This item has {power1} power."
        if params['power2'] != '':
            prompt += " This item has {power2} power."
        if params['affinity1'] != '':
            prompt += " This item has {affinity1} affinity."
        if params['affinity2'] != '':
            prompt += " This item has {affinity2} affinity."
        if params['target_class'] != '':
            prompt += " This item is designed to be useful to players of the {target_class} class."
        if params['origin_race'] != '':
            prompt += " This item was created by the {origin_race} race."
        if params['alignment'] != '':
            prompt += " This item is must effective when used by one with {alignment} alignment."
        
        params = st.session_state['params']
        prompt = prompt.format(**params)
        openai_widget = OpenAIGenerationWidget(prompt)
        