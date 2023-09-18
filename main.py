# Importing necessary libraries
import streamlit as st

# Importing other files for setup and functionalities
from setup_st import *
from helper_functions import *
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

# Main chat loop to display messages
for message in st.session_state.messages:
    if message['role'] == 'assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    elif message['role'] == 'user':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input and generate response
if prompt := st.chat_input("How would you like to reply?"):

    # Append the user's message to the 'messages' list in session state.
    if prompt != "":
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Add user's message to the chat history
    with st.chat_message(message["role"]):
        st.markdown(prompt)

    # Increment total message count
    st.session_state['message_count'] += 1
    
    # Call either generate_response or generate_response_index based on st.session_state['use_index']
    if st.session_state.get('use_index', False):
        index = load_data()
        chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
        response_generated = generate_response_index(
            "You are an expert consultant who is great at assisting users with whatever query they have",
            st.session_state.messages,
            st.session_state['model_name'],
            st.session_state['temperature'],
            chat_engine
        )
    else:
        response_generated = generate_response(
            "You are an expert consultant who is great at assisting users with whatever query they have",
            st.session_state.messages,
            st.session_state['model_name'],
            st.session_state['temperature']
        )
    
    # Create spinner to indicate to the user that the assistant is generating a response
    with st.spinner('CoPilot is thinking...'):
        # Create a chat message box for displaying the assistant's response
        
        with st.chat_message("assistant"):
            # Initialize an empty string to construct the full response incrementally
            full_response = ""
            # Create an empty placeholder to stream the assistant's response
            message_placeholder = st.empty()
            
            # Loop through the generator response
            for response in response_generated:
                # If the full_response is not empty, display it and save to message history
                if full_response:
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                # Reset full_response and create a new empty placeholder
                full_response = ""
                message_placeholder = st.empty()
                # Break the content into chunks of 10 words each
                chunks = response["content"].split(' ')
                full_response = ""
                
                # Loop through the chunks to simulate a 'typing' effect
                for i in range(0, len(chunks), 10):
                    # Join the next 10 words to form a chunk
                    chunk = ' '.join(chunks[i:i+10])
                    # Add the chunk to the full response string
                    full_response += chunk + " "  # Add a space at the end of each chunk
                    # Display the currently generated text followed by a 'typing' cursor
                    message_placeholder.markdown(full_response + "▌")
                    # Wait for a small amount of time to simulate the typing effect
                    time.sleep(0.2)
                    
            # Remove the 'typing' cursor and display the final full response
            message_placeholder.markdown(full_response)
            
            # Add the assistant's final full response to the session state message history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    # Code to update the progress bar; assuming a message cap of 10 messages
    current_progress = st.progress(st.session_state['message_count'] / 10)
