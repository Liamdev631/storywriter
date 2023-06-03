from abc import abstractstaticmethod
import os
os.environ['OPENAI_API_KEY'] = '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'
from langchain import OpenAI, PromptTemplate
from langchain.llms import OpenAI, OpenAIChat
from langchain.llms.base import BaseLLM
import streamlit as st
import random

st.title('Storywriter')

option = st.selectbox(
    'DnD',
    ('Characters', 'Quests', 'Worlds'))

class Generator():
    @abstractstaticmethod
    def OnGenerate(self, params: dict):
        pass

class WorldGenerator(Generator):
    @staticmethod
    def OnGenerate(llm, params: dict):
        template: str = "You are a DnD Dungeon Master. Design a {world_age} year old world for a {edition} edition campaign. In this world, magic is available to {magic_prevalance}% of the population."
        prompt: str = PromptTemplate.from_template(template=template).format(**params)
        st.header('Prompt')
        st.markdown(prompt)
        
        result: str = llm(prompt)
        st.header('Result')
        st.markdown(result)
        
class CharacterGenerator(Generator):
    @staticmethod
    def OnGenerate(llm, params: dict):
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
        """
        prompt: str = PromptTemplate.from_template(template=template).format(**params)
        st.header('Prompt')
        st.markdown(prompt)
        
        result: str = llm(prompt)
        st.header('Result')
        st.markdown(result)

#llm: BaseLLM = OpenAIChat(client=None, model_name='gpt-3.5-turbo')
llm: BaseLLM = OpenAI(client=None, model_name='text-davinci-003', max_tokens=1024, disallowed_special=['Random'])

races_list = ('None', 'Random', 'Aarakocra', 'Aasimar', 'Bugbear', 'Centaur', 'Changeling', 'Dragonborn', 'Dwarf', 'Elf', 'Firbolg', 'Genasi', 'Githyanki', 'Githzerai', 'Goblin', 'Goliath', 'Grung', 'Halfling', 'Harengon', 'Hobgoblin', 'Human', 'Kalashtar', 'Kenku', 'Kobold', 'Leonin', 'Lizardfolk', 'Loxodon', 'Minotaur', 'Orc', 'Owlin', 'Satyr', 'Shifter', 'Simic Hybrid', 'Tabaxi', 'Tiefling', 'Tortle', 'Triton', 'Vedalken', 'Verdan', 'Warforged', 'Yuan-ti Pureblood')

alignment_list = ('Random', 'Lawful Good', 'Neutral Good', 'Chaotic Good',
                  'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
                  'Lawful Evil', 'Neutral Evil', 'Chaotic Evil')

class_list = ('None', 'Random', 'Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 
              'Rogue', 'Sorcerer', 'Warlock', 'Wizard', 'Alchemist', 'Blood Hunter', 'Cavalier', 'Chronurgist', 
              'Circle of Spores Druid', 'Echo Knight', 'Graviturgist', 'Gunslinger', 'Hexblade', 'Inquisitive', 
              'Mystic', 'Oath of the Watchers Paladin', 'Order Domain Cleric', 'Psi Knight', 'Rune Knight', 
              'Samurai', 'Swarmkeeper Ranger', 'Way of the Astral Self Monk', 'Wildfire Druid', 'Armorer Artificer', 
              'Bladesinging Wizard', 'Circle of Stars Druid', 'College of Creation Bard', 'Genie Warlock', 
              'Oath of Glory Paladin', 'Path of Wild Magic Barbarian', 'Phantom Rogue', 'Psi Warrior Fighter', 
              'Soulknife Rogue', 'Twilight Domain Cleric')

background_list = ('Random', 'Acolyte', 'Anthropologist', 'Archaeologist', 'Charlatan', 'City Watch', 'Clan Crafter', 
                   'Cloistered Scholar', 'Courtier', 'Criminal', 'Entertainer', 'Faction Agent', 'Far Traveler', 
                   'Folk Hero', 'Guild Artisan', 'Haunted One', 'Hermit', 'Inheritor', 'Knight of the Order', 
                   'Mercenary Veteran', 'Noble', 'Outlander', 'Pirate', 'Sage', 'Sailor', 'Soldier', 
                   'Urban Bounty Hunter', 'Urchin', 'Volstrucker Agent', 'Gladiator', 'Guild Merchant', 
                   'Highway Robber', 'House Agent', 'Innkeeper', 'Investigator', 'Knight', 'Marine', 
                   'Medic', 'Miner', 'Plaintiff', 'Refugee', 'Rival Intern', 'Rustic', 'Shipwright', 
                   'Smuggler', 'Spy', 'Squire', 'Student of Magic', 'Survivor', 'Trade Sheriff', 
                   'Veteran of the Psychic Wars', 'Vizier', 'Wanderer', 'Waterdhavian Noble')

def random_selection(parameter, options):
    if parameter == 'Random':
        temp_list = [option for option in options if option not in ['None', 'Random']]
        return random.choice(temp_list)
    else:
        return parameter

def load_tool(selected_option):
    p: dict = {}
    
    if selected_option == 'Worlds':
        p['edition'] = st.selectbox('Edition', ('5th', '4th', '3rd', '2nd', '1st'))
        p['magic_prevalance'] = st.slider('Magic Prevalance', value=10, min_value=1, max_value=100, step=1)
        p['world_age'] = st.slider('World Age (years)', value=5000, min_value=0, max_value=10000, step=100)
        if st.button('Generate'):
            WorldGenerator.OnGenerate(llm, p)
            
    if selected_option == 'Characters':
        col1, col2 = st.columns(2)
        
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
            p['dexterity'] = st.slider('Dexterity', value=5, min_value=1, max_value=20)
            p['strength'] = st.slider('Strength', value=5, min_value=1, max_value=20)
            p['constitution'] = st.slider('Constitution', value=5, min_value=1, max_value=20)
            p['intelligence'] = st.slider('Intelligence', value=5, min_value=1, max_value=20)
            p['charisma'] = st.slider('Charisma', value=5, min_value=1, max_value=20)
            p['wisdom'] = st.slider('Wisdom', value=5, min_value=1, max_value=20)
        
        if st.button('Generate'):
            CharacterGenerator.OnGenerate(llm, p)

load_tool(option)


