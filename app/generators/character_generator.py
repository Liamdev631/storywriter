from widgets import OpenAIGenerationWidget
import streamlit as st
from utils import load_list
from openai import ChatCompletion
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

class CharacterGenerator():
    def __init__(self):
        if not 'character' in st.session_state:
            st.session_state['character'] = {}
        tab_design, tab_sheet = st.tabs(['Design', 'Sheets'])
        with tab_design:
            gui_col, generator_col = st.columns(2) 
            with gui_col:
                self.draw_designer_gui()

            with generator_col:
                self.draw_designer_result()
                    
        with tab_sheet:
            gui_col, generator_col = st.columns(2) 
            with gui_col:
                self.draw_sheets_gui()

            with generator_col:
                self.draw_sheets_result()
                
    def draw_designer_gui(self):
        st.title('DnD Character Generator')
        
        params = {}
        
        races_list:         list[str] = load_list("app/resources/dnd/races.csv")
        alignment_list:     list[str] = load_list("app/resources/dnd/alignments.csv")
        class_list:         list[str] = load_list("app/resources/dnd/classes.csv")
        background_list:    list[str] = load_list("app/resources/dnd/backgrounds.csv")

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
    
    def draw_designer_result(self):
        if st.button('Generate', type='primary', key='btn_gen_character_design'):
            st.session_state['character'] = {}
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
            
            Please fill the followign character sheet template with details of this new character, keeping the exact same formatting. Do not repeat any of this information verbatum, only append original story.
            """
            
            params = st.session_state['params']
            prompt = prompt.format(**params)
            openai_widget = OpenAIGenerationWidget(prompt)
            st.session_state['character']['design'] = openai_widget.result
        else:
            if 'design' in st.session_state['character']:
                design = st.session_state['character']['design']
                st.markdown(design)
                st.download_button(label='Save', data=design, mime='txt')
                
        
    def draw_sheets_gui(self):
        if 'design' in st.session_state['character']:
            design = st.session_state['character']['design']
            st.markdown(design)
    
    def draw_sheets_result(self):
        if not 'design' in st.session_state['character']:
            st.markdown('Please create a character design first!')
            return
        
        if st.button('Generate', type='primary', key='btn_gen_character_sheet'):
            design = st.session_state['character']['design']
            template = ""
            with open('app/templates/DWTemplateCharacterSheet.tex') as f:
                template = f.read()
                f.close()
            params = st.session_state['params']
            parser = PydanticOutputParser(pydantic_object=DnDCharacter)
            format_instructions = parser.get_format_instructions()
            #st.markdown(st.session_state['character']['design'])
            prompt = f"""You are an AI assistant designs Dungeons and Dragons character sheets. Given the design document [[DESIGN]], and the user-specified character attributes document [[ATTRIBUTES]] produce a full-formed character sheet. Do not include any comments in your response. Fill the template with as much original information from the template as possible, and using creativity to replace the rest of the fields in a reasonable manner.\n{format_instructions}
            
            [[DESIGN]]
            {design}
            
            [[ATTRIBUTES]]
            {params}
            """
            openai_api_key: str = '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'
            response = ChatCompletion.create(model='gpt-3.5-turbo', n=1, temperature=1.0, messages=[{'role': 'user', 'content': prompt}], api_key=openai_api_key)
            result: str = response.choices[0]["message"]["content"] # type: ignore
            parsed = parser.parse(result)
            st.session_state['character']['sheet'] = parsed
            
        if 'sheet' in st.session_state['character']:
            sheet = st.session_state['character']['sheet']
            st.write(sheet)
            
            from pydantic import BaseModel
from typing import List, Optional

class AbilityScores(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

class Skills(BaseModel):
    acrobatics: int
    animal_handling: int
    arcana: int
    athletics: int
    deception: int
    history: int
    insight: int
    intimidation: int
    investigation: int
    medicine: int
    nature: int
    perception: int
    performance: int
    persuasion: int
    religion: int
    sleight_of_hand: int
    stealth: int
    survival: int

class Equipment(BaseModel):
    item_name: str
    quantity: int

class Spell(BaseModel):
    spell_name: str
    spell_level: int

class DnDCharacter(BaseModel):
    character_name: str
    class_name: str
    level: int
    race: str
    alignment: str
    experience_points: int
    hit_points: int
    proficiency_bonus: int
    armor_class: int
    speed: int
    ability_scores: AbilityScores
    saving_throws: AbilityScores
    skills: Skills
    languages: List[str]
    features_traits: List[str]
    equipment: List[Equipment]
    spells: Optional[List[Spell]]
    backstory: Optional[str]
    notes: Optional[str]

        

