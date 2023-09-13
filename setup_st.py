import streamlit as st

def set_design():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("logo.png", use_column_width=True)  # Make sure this image exists

    st.markdown("<p style='text-align: center; font-size: 16px;'><b>[YOUR TITLE HERE]</b></p>", unsafe_allow_html=True)

def initialize_session_state():
    st.session_state.setdefault('current_stage_index', 0)
    st.session_state.setdefault('message_count', 0)
    st.session_state.setdefault('model_name', "gpt-3.5-turbo")
    st.session_state.setdefault('temperature', 0.3)

# 3. Initialize your sidebar
def sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { 
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True) # Optional HTML which hides the sidebar in your app upon load
    
    st.markdown('#') # Adds an empty space
    global logo_placeholder
    logo_placeholder = st.sidebar.empty() 
    static_logo()
    st.sidebar.markdown("""
    <h1 style='color: black; font-size: 28px;'>CoPilot Configuration</h1>
    """, unsafe_allow_html=True)

# 4. Setup clear button on the sidebar. Known bug that initial message disappears after first input post-clear
def clear_button():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    # Clear the conversation
    if clear_button:
        # Clear the conversation
        st.session_state['history'] = []
        st.session_state['initial_message'] = get_initial_message()
        st.session_state['messages'] = [
            {"role": "system", "content": st.session_state['initial_message']}
        ]
        with st.chat_message("assistant", avatar=bruce) as chat:
            st.markdown(st.session_state['initial_message'])
        st.session_state['current_stage_index'] = 0
        st.session_state['message_count'] = 0
        st.session_state['messages_per_stage'] = {stage: 0 for stage in stages}
        st.session_state['completed'] = False

# 5. Setup download_convo function to track the conversation for download functionality
def download_convo():
    if 'messages' in st.session_state and len(st.session_state['messages']) > 0:
        full_conversation = "\n".join([
            f"\n{'-'*20}\n"
            f"Role: {msg['role']}\n"
            f"{'-'*20}\n"
            f"{msg['content']}\n"
            for msg in st.session_state['messages']
        ])
        return full_conversation
    else:
        st.warning("There aren't enough messages in the conversation to download it. Please refresh the page")
        return ""

# 6. Setup download button
def download_button():
    full_conversation = download_convo()  # Get the full_conversation string
    st.sidebar.download_button(
        label="Download conversation",
        data=full_conversation,
        file_name='conversation.txt',
        mime='text/plain'
    )

