import streamlit as st
import openai

class Dalle2GenerationWidget():
    def __init__(self, prompt):
        openai_api_key: str = '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'
        #params: dict[str,str] = st.session_state['params']
        #prompt: str = 'realistic, ' + str(params.values())
        #st.markdown(f'Generating image from{prompt}')
        response = openai.Image.create(openai_api_key, n=1, size='256x256', prompt=prompt)
        image_url: str = response['data'][0]['url'] # type: ignore
        st.image(image_url)