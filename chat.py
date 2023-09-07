import json
import torch
import datetime
import requests
import streamlit as st

# Reading:
# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
# https://docs.streamlit.io/library/api-reference/chat

def run_prompt(model, prompt):
    r = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': prompt
        }
    )
    return [json.loads(row) for row in r.text.splitlines()]

# Using object notation
model_selection = st.sidebar.selectbox(
    'Model',
    (
        'llama2:latest',
        'llama2-uncensored:latest',
        'codeup:latest',
        'codeup:13b',
        'codeup:13b-llama2',
        'nous-hermes:latest',
        'vicuna:latest',
        'wizard-math:latest',
        'wizard-vicuna:latest',
        'wizard-vicuna-uncensored:latest',
        'wizardlm:latest',
        'wizardlm-uncensored:latest',
        'stable-beluga:latest',
        'open-orca-platypus2:latest',
        'everythinglm:latest'
    )
)

if model_selection:
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message['role'] == 'chatbot':
            with st.chat_message(message['role']):
                st.markdown(message['content'])
        else:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    # React to user input
    if prompt := st.chat_input(''):
        # Display user message in chat message container
        st.chat_message('user').text(f'''
        user@{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}:

        {prompt}
        ''')
        
        # Add user message to chat history
        st.session_state.messages.append({'role': 'user', 'content': prompt})
       
        # Display chatbot response in chat message container
        with st.spinner(f'querying {model_selection}...'):
            response = run_prompt(model_selection, prompt)
        
        with st.chat_message('chatbot'):
            chat_response = f"chatbot@{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}:\n\n"
            for line in response:
                if line['done'] != True and 'response' in line:
                    chat_response += line['response']
                
            st.markdown(chat_response)
        
        # Add chatbot response to chat history
        st.session_state.messages.append({'role': 'chatbot', 'content': chat_response})