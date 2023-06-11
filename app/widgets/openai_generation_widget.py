from generators import Generator
import openai
import streamlit as st
import openai
from openai.error import AuthenticationError, RateLimitError

class OpenAIGenerationWidget:
    def __init__(self, generator: Generator, prompt: str):
        openai_api_key: str = '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'
        whole_response: str = ""
        try:
            combined = []
            result_box = st.empty()
            result = openai.ChatCompletion.create(model='gpt-3.5-turbo', n=1, temperature=1.0, stream=True, messages=[{'role': 'user', 'content': prompt}], api_key=openai_api_key)
            for response_chunk in result:
                response_text = response_chunk['choices'][0]['delta'] # type: ignore
                answer = response_text.get('content', '')
                combined.append(answer) # type: ignore
                whole_response = ''.join(combined)
                result_box.markdown(whole_response, unsafe_allow_html=False)
        except AuthenticationError as e:
            if e.code == 401:
                st.warning("Invalid Authentication. Ensure the correct API key and requesting organization are being used.")
                st.warning("Incorrect API key provided. Ensure the API key used is correct, clear your browser cache, or generate a new one.")
                st.warning("You must be a member of an organization to use the API. Contact us to get added to a new organization or ask your organization manager to invite you to an organization.")
            elif e.code == 429:
                st.warning("Rate limit reached for requests. Pace your requests. Read the Rate limit guide.")
                st.warning("You exceeded your current quota, please check your plan and billing details. Apply for a quota increase.")
                st.warning("The engine is currently overloaded, please try again later. Please retry your requests after a brief wait.")
            elif e.code == 500:
                st.warning("The server had an error while processing your request. Retry your request after a brief wait and contact us if the issue persists. Check the status page.")
        except RateLimitError:
            st.warning('Rate limit reached. Just wait a minute and try again, because of the key everyone is sharing.')
        st.download_button(label='Save', data=whole_response, mime='txt')
        # messages = [
        #     {'role': 'user', 'content': 'From the following text, describe the physical appearance of the subject as accurately and descriptively as possible in less than 50 words. Do not include ANY non-visual information. If no visual information exists, you may create it yourself based on the nature of the subject:'},
        #     {'role': 'user', 'content': whole_response}
        # ]
        # caption_response = openai.ChatCompletion.create(model='gpt-3.5-turbo', n=1, temperature=1.0, messages=messages, api_key=openai_api_key)
        # caption = caption_response.choices[0]["message"]["content"] # type: ignore
        
        # image_response = openai.Image.create(n=1, size='256x256', prompt=caption, api_key=openai_api_key)
        # image_url: str = image_response['data'][0]['url'] # type: ignore
        # st.image(image_url, caption=caption)