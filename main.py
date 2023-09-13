import streamlit as st
from setup_st import set_design, initialize_session_state, sidebar, clear_button, download_button, get_user_config
from helper_functions import generate_response
from index_functions import construct_index

# Initialize session state
initialize_session_state()

# Initialize UI/UX
set_design()
sidebar()
get_user_config()

# Initialize knowledge base index
directory_path = "/path/to/your/documents"  # Make sure this path exists
index = construct_index(directory_path)

# Main chatbot logic
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate chatbot response
    if len(st.session_state.messages) >= 2:
        for response in generate_response(
                prompt, st.session_state.messages, index,
                st.session_state['model_name'], st.session_state['temperature'],
                st.session_state['current_stage_index']):
            st.session_state.messages.append({"role": "assistant", "content": response['content']})
    else:
        st.warning("Not enough conversation history.")

    clear_button()
    download_button()
