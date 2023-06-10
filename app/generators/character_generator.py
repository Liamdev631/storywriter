from .generator import Generator
import streamlit as st
from utils import load_list

class CharacterGenerator(Generator):
    def load_gui(self):
        st.title('DnD Character Generator')
        
        params = {}
        
        races_list:         list[str] = load_list("app/resources/dnd/races.csv")
        alignment_list:     list[str] = load_list("app/resources/dnd/alignments.csv")
        class_list:         list[str] = load_list("app/resources/dnd/classes.csv")
        background_list:    list[str] = load_list("app/resources/dnd/backgrounds.csv")
        editions_list:      list[str] = load_list("app/resources/dnd/editions.csv")

        col1, col2, col3 = st.columns(3)
        
        with col1:
            params['age'] = st.number_input('Age', value=20, min_value=1)
            params['race_primary'] = st.selectbox('Primary Race', races_list, index=races_list.index('Human'))
            params['race_secondary'] = st.selectbox('Secondary Race', races_list, index=races_list.index(''))
            params['alignment'] = st.selectbox('Alignment', alignment_list, index=alignment_list.index(''))
            params['primary_class'] = st.selectbox('Primary Class', class_list, index=class_list.index('Bard'))
            params['secondary_class'] = st.selectbox('Secondary Class', class_list, index=class_list.index(''))
            params['background'] = st.selectbox('Background', background_list, index=background_list.index('Acolyte'))
            
        with col2:
            params['dexterity'] = st.slider('Dexterity', value=5, min_value=1, max_value=20)
            params['strength'] = st.slider('Strength', value=5, min_value=1, max_value=20)
            params['constitution'] = st.slider('Constitution', value=5, min_value=1, max_value=20)
            params['intelligence'] = st.slider('Intelligence', value= 5, min_value=1, max_value=20)
            params['charisma'] = st.slider('Charisma', value=5, min_value=1, max_value=20)
            params['wisdom'] = st.slider('Wisdom', value=5, min_value=1, max_value=20)
                
        with col3:
            params['openness'] = st.slider('Openness', value=50, min_value=0, max_value=100, step=5)
            params['conscientiousness'] = st.slider('Conscientiousness', value=50, min_value=0, max_value=100, step=5)
            params['extraversion'] = st.slider('Extraversion', value=50, min_value=0, max_value=100, step=5)
            params['agreeableness'] = st.slider('Agreeableness', value=50, min_value=0, max_value=100, step=5)
            params['neuroticism'] = st.slider('Neuroticism', value=0, min_value=0, max_value=100, step=5)

        st.session_state['params'] = params
    
    @staticmethod
    def generate(params: dict[str,str]) -> str:
        prompt: str = """
        You are an expert DnD Dungeon Master who helps players flesh out their character designs. Given a rough idea of what they're looking for, you help players dreams meet reality.
        Design a character for a 5th edition DnD campaign with the stats listed below. Be sure to include a deep backstory. What is their name? Who were the characters parents? Where is their hometown? What were the two most significant events in their life? What quirks does the character have? What is their alignment and personality? Is your character religious? If so what Deity? What event in their life caused them to choose this particular god or goddess? What profession is the character? What languages do they speak? What are the characters hopes and dreams for the future?
        
        Primary Race: {race_primary}.
        Secondary Race: {race_secondary}.
        Age: {age} years).
        Alignment: {alignment}.
        Primary Class: {primary_class}.
        Secondary Class: {secondary_class}.
        Background: {background}.
        
        Stats:
        Dexterity: {dexterity}.
        Strength: {strength}.
        Constitution: {constitution}.
        Intelligence: {intelligence}.
        Charistma: {charisma}.
        Wisdom: {wisdom}.
        
        Personality traits:
        Openness: {openness}%.
        Conscientiousness: {conscientiousness}%.
        Extraversion: {extraversion}%.
        Agreeableness: {agreeableness}%.
        Neuroticism: {neuroticism}%.
        """
        
        return prompt.format(**params)

