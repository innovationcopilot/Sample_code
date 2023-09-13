import openai
import streamlit as st

# Initialize OpenAI API (Replace with your actual API key)
openai.api_key = "your_actual_api_key_here"

def generate_response(prompt, history, index, model_name, temperature, stage):
      chatbot_message = history[-1]['content']
      user_idea = history[1]['content']
  
    else:
        return {"type": "error", "content": "Not enough conversation history to generate a response."}
    
    full_prompt = f"{prompt}\n\
    ### The original idea: {user_idea}. \n\
    ### Your latest message to me: {chatbot_message}. \n\
    ### Previous conversation history for context: {history}"

    if st.session_state.get('user_context_flag', True):
        full_prompt += f"\n### Additional user context to further refine your responses: {st.session_state['user_context']}"

    relevant_info = index.query(user_idea)
    full_prompt += f"\n### Relevant data from documents: {relevant_info}"

    response_generator = openai.ChatCompletion.create(
        model=model_name,
        temperature=temperature,
        messages=[
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    full_response = ""
    for response in response_generator:
        if 'content' in response['choices'][0]['delta']:
            full_response += response['choices'][0]['delta']['content']

    yield {"type": "response", "content": full_response}
