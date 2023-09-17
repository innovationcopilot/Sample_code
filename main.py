# Importing necessary libraries and modules
import streamlit as st

# Importing custom modules for setup and functionalities
from setup_st import *
from helper_functions import generate_response
from index_functions import *

# Initialize session state variables if they don't exist
initialize_session_state()

# Setup Streamlit UI/UX elements
set_design()
sidebar()
get_user_config()
clear_button()
download_button()

# Setting up environment variables for OpenAI API key
if 'api_key' in st.session_state and st.session_state['api_key']:
    openai.api_key = st.session_state['api_key']
else:
    st.sidebar.warning("OpenAI API key not provided. Please enter it in the sidebar.")

# Initialize the knowledge base index
if 'directory_path' in st.session_state and st.session_state['directory_path']:
    directory_path = st.session_state['directory_path']
    index = construct_index(directory_path)
else:
    st.sidebar.warning("Directory path isn't uploaded to serve as chatbot knowledge base. Please upload it in sidebar if you'd like to query information.")

# Main chat loop to display messages
for message in st.session_state.messages:
    if message['role'] == 'assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    elif message['role'] == 'user':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How would you like to reply?"):
    
    # Add user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message(message["role"]):
        st.markdown(prompt)

    # Increment total message count
    st.session_state['message_count'] += 1
    
    # Call generate_response function to get chatbot's reply
    # This function is assumed to be defined in your helper_functions.py
    # response_generated = generate_response("You are an expert consultant who is great at assisting users with whatever query they have", st.session_state.messages, index, st.session_state['model_name'], st.session_state['temperature'])
    response_generated = generate_response("You are an expert consultant who is great at assisting users with whatever query they have", st.session_state.messages, st.session_state['model_name'], st.session_state['temperature'])
    
    # Create spinner while response is generating
    with st.spinner('CoPilot is thinking...'):
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in response_generator:
                full_response += response['content']
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Code to update the progress bar
    # For the sake of this example, I'm incrementing it by 10% each time and assuming a message cap of 10 messages
    current_progress = st.progress(st.session_state['message_count'] / 10)
