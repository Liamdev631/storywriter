from generators import Generator
import openai
import streamlit as st
import openai
from openai.error import AuthenticationError, RateLimitError

class OpenAIGenerationWidget:
    def __init__(self, generator: Generator):
        if st.button('Generate', type='primary'):
            wait_message = st.markdown("----Generating! Please wait 15-30 seconds.----")
            try:
                combined = []
                result_box = st.empty()
                prompt = generator.generate(st.session_state['params'])
                result = openai.ChatCompletion.create(model='gpt-3.5-turbo', temperature=1.0, stream=True, messages=[{'role': 'user', 'content': prompt}])
                for response_chunk in result:
                    response_text = response_chunk['choices'][0]['delta'] # type: ignore
                    answer = response_text.get('content', '')
                    combined.append(answer) # type: ignore
                    result_box.markdown(''.join(combined), unsafe_allow_html=False)
                wait_message.empty()
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