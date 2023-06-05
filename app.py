from abc import abstractstaticmethod
import os
os.environ['OPENAI_API_KEY'] = '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'
from langchain import OpenAI, PromptTemplate
from langchain.llms import OpenAI, OpenAIChat
from langchain.llms.base import BaseLLM
import streamlit as st
import random
import pandas as pd

st.set_page_config(layout="wide")

st.title('Storywriter')

option = st.selectbox(
    'DnD',
    ('Characters', 'Quests', 'Worlds'))

class Generator():
    @staticmethod
    def generate(llm: BaseLLM,  params: dict):
        pass

class WorldGenerator(Generator):
    @staticmethod
    def generate(llm: BaseLLM, params: dict):
        template: str = "You are a DnD Dungeon Master. Design a {world_age} year old world for a {edition} edition campaign. In this world, magic is available to {magic_prevalance}% of the population."
        prompt: str = PromptTemplate.from_template(template=template).format(**params)
        result: str = llm(prompt)
        st.markdown(result)
        
class CharacterGenerator(Generator):
    @staticmethod
    def generate(llm, params: dict):
        template: str = """
        You are a DnD Game Master. Design a character for a {edition} edition campaign with the stats listed below. Be sure to include a deep backstory. What is their name? Who were the characters parents, are they alive? If not, how did they die. Where is their hometown? What were the two most significant events in their life? What quirks does the character have? What is their alignment and personality? Is your character religious? If so what Deity? What event in their life caused them to choose this particular god or goddess? What profession is the character? What languages do they speak? What are the characters hopes and dreams for the future? Your response MUST be formatted in Markdown.
        
        (Primary Race: {race_primary}).
        (Secondary Race: {race_secondary}).
        (Age: {age} years).
        (Alignment: {alignment}).
        (Primary Class: {primary_class}).
        (Secondary Class: {secondary_class}).
        (Background: {background}).
        
        (Dexterity: {dexterity}).
        (Strength: {strength}).
        (Constitution: {constitution}).
        (Intelligence: {intelligence}).
        (Charistma: {charisma}).
        (Wisdom: {wisdom}).
        
        Personality traits: 
        (Openness: {openness}%).
        (Conscientiousness: {conscientiousness}%).
        (Extraversion: {extraversion}%).
        (Agreeableness: {agreeableness}%).
        (Neuroticism: {neuroticism}%).
        """
        prompt: str = PromptTemplate.from_template(template=template).format(**params)
        # st.header('Prompt')
        # st.markdown(prompt)
        
        result: str = llm(prompt)
        st.header('Result')
        st.markdown(result)

#llm: BaseLLM = OpenAIChat(client=None, model_name='gpt-3.5-turbo')
llm: BaseLLM = OpenAI(client=None, model_name='text-davinci-003', max_tokens=1024, disallowed_special=['Random'])

races_list:         list[str] = pd.read_csv("resources/dnd/races.csv", header=None, keep_default_na=False)[0].to_list()
alignment_list:     list[str] = pd.read_csv("resources/dnd/alignments.csv", header=None, keep_default_na=False)[0].to_list()
class_list:         list[str] = pd.read_csv("resources/dnd/classes.csv", header=None, keep_default_na=False)[0].to_list()
background_list:    list[str] = pd.read_csv("resources/dnd/backgrounds.csv", header=None, keep_default_na=False)[0].to_list()

def random_selection(parameter, options):
    if parameter == 'Random':
        temp_list = [option for option in options if option not in ['None', 'Random']]
        return random.choice(temp_list)
    else:
        return parameter

def load_tool(selected_option):
    p: dict = {}
    col1_outer, col2_outer = st.columns(2)
    
    with col1_outer:
        if selected_option == 'Worlds':
            p['edition'] = st.selectbox('Edition', ('5th', '4th', '3rd', '2nd', '1st'))
            p['magic_prevalance'] = st.slider('Magic Prevalance', value=10, min_value=1, max_value=100, step=1)
            p['world_age'] = st.slider('World Age (years)', value=5000, min_value=0, max_value=10000, step=100)
            if st.button('Generate'):
                WorldGenerator.generate(llm, p)
                
        if selected_option == 'Characters':
            col1, col2, col3 = st.columns(3)
            
            with col1:
                p['edition'] = st.selectbox('Edition', ('5th', '4th', '3rd', '2nd', '1st'))
                p['age'] = st.number_input('Age', value=20, min_value=1)
                p['race_primary'] = st.selectbox('Primary Race', races_list, index=races_list.index('Human'))
                p['race_secondary'] = st.selectbox('Secondary Race', races_list, index=races_list.index('None'))
                p['alignment'] = st.selectbox('Alignment', alignment_list, index=alignment_list.index('Random'))
                p['primary_class'] = st.selectbox('Primary Class', class_list, index=class_list.index('Random'))
                p['secondary_class'] = st.selectbox('Secondary Class', class_list, index=class_list.index('None'))
                p['background'] = st.selectbox('Background', background_list, index=background_list.index('Random'))
                
                # Randomly fill parameters designated as such
                p['race_primary'] = random_selection(p['race_primary'], races_list)
                p['race_secondary'] = random_selection(p['race_secondary'], races_list)
                p['alignment'] = random_selection(p['alignment'], alignment_list)
                p['primary_class'] = random_selection(p['primary_class'], class_list)
                p['secondary_class'] = random_selection(p['secondary_class'], class_list)
                p['background'] = random_selection(p['background'], background_list)
            
            with col2:
                p['dexterity'] = st.slider('Dexterity', value=5, min_value=1, max_value=20, help="Dexterity measures agility, reflexes, and balance. This is important for characters that rely on speed and precision.")
                
                p['strength'] = st.slider('Strength', value=5, min_value=1, max_value=20, help="Strength measures physical power and carrying capacity. This is important for characters that engage in hand-to-hand combat.")
                
                p['constitution'] = st.slider('Constitution', value=5, min_value=1, max_value=20, help="Constitution measures health, stamina, and vital force. This is important for characters that need to withstand damage or endure harsh conditions.")
                
                p['intelligence'] = st.slider('Intelligence', value=5, min_value=1, max_value=20, help="Intelligence measures mental acuity, information recall, and analytical skill. This is important for characters that rely on knowledge and magic.")
                
                p['charisma'] = st.slider('Charisma', value=5, min_value=1, max_value=20, help="Charisma measures ability to lead, and influence others. This is important for characters that rely on personal magnetism and diplomacy.")
                
                p['wisdom'] = st.slider('Wisdom', value=5, min_value=1, max_value=20, help="Wisdom measures awareness, intuition, and insight. This is important for characters that rely on perception and wisdom-based magic.")

                
            with col3:
                p['openness'] = st.slider('Openness', value=50, min_value=0, max_value=100, step=5, help="This trait features characteristics such as imagination and insight. A high score in this trait can represent a character who is creative, adventurous, and curious. A low score can represent a character who is practical, conventional, and prefers routine.")

                p['conscientiousness'] = st.slider('Conscientiousness', value=50, min_value=0, max_value=100, step=5, help="This trait is characterized by high levels of thoughtfulness, good impulse control, and goal-directed behaviors. High scorers are organized and mindful of details, while low scorers may be more spontaneous and disorganized.")

                p['extraversion'] = st.slider('Extraversion', value=50, min_value=0, max_value=100, step=5, help="This trait includes characteristics such as excitability, sociability, talkativeness, assertiveness, and high amounts of emotional expressiveness. A high scorer could be outgoing and energetic, while a low scorer might be more solitary or reserved.")

                p['agreeableness'] = st.slider('Agreeableness', value=50, min_value=0, max_value=100, step=5, help="This trait includes attributes such as trust, altruism, kindness, affection, and other prosocial behaviors. Characters with high agreeableness tend to be cooperative and considerate, while those with low agreeableness may be more competitive and even manipulative.")

                p['neuroticism'] = st.slider('Neuroticism', value=50, min_value=0, max_value=100, step=5, help="This trait is characterized by sadness, moodiness, and emotional instability. Individuals who score high in neuroticism often experience mood swings, anxiety, irritability, and sadness. Those who score low in neuroticism tend to be more stable and emotionally resilient.")
    
    with col2_outer:
        if st.button('Generate'):
            CharacterGenerator.generate(llm, p)

load_tool(option)


