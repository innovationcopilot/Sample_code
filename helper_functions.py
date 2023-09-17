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

#####additional, specific functions I had in the Innovation CoPilot for inspiration:

# Function returns a random thanks phrase to be used as part of the CoPilots reply
# Note: Requires a dictionary of 'thanks phrases' to work properly
def get_thanks_phrase():
    selected_phrase = random.choice(thanks_phrases)
    return selected_phrase

# Function to randomize initial message of CoPilot
# Note: Requires a dictionary of 'initial messages' to work properly
def get_initial_message():
    initial_message = random.choice(initial_message_phrases)
    print(f"initial message returned...")
    return initial_message

# Function adds relevant 'mode-specific' context to the prompt if this has been selected in the Sidebar. 
# Note: The mode selection isn't included in the example code
'''def mode_prompt():
    if st.session_state['mode'] == "Standard":
        return ""
    elif st.session_state['mode'] == "Tough":
        return "I've selected tough validation mode and want you to be far more critical and less empathetic in all of your responses."
    else:
        return "I've selected easy validation mode and want you to be far less critical and more empathetic in all of your responses."
'''

# Function to add relevant stage specific context into prompt
# def get_stage_prompt(stage):

# Function to generate the summary; used in part of the response
'''def generate_summary(model_name, temperature, summary_prompt):
    summary_response = openai.ChatCompletion.create(
        model=model_name,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "You are an expert at summarizing information effectively and making others feel understood"},
            {"role": "user", "content": summary_prompt},
        ]
    )
    summary = summary_response['choices'][0]['message']['content']
    print(f"summary: {summary}, model name: 'gpt-4', temperature: {temperature})")
    return summary
    '''

# Function to grade the response based on length, relevancy, and depth of response
# def grade_response(user_input, assistant_message, idea):

# Function used to generate a final 'report' at the end of the conversation, summarizing the convo and providing a final recomendation
# def generate_validation_report():

# Function used to enable 'summary' mode in wihch the CoPilot only response with bullet points rather than paragraphs
'''def transform_bullets(content):
    try:
        prompt = f"Summarize the following content in 3 brief bullet points while retaining the structure and conversational tone (using wording like 'you' and 'your idea'):\n{content}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=.2,
            messages=[
                {"role": "system", "content": prompt}
            ],
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(response)
        print("Error in transform_bullets:", e)
        return content  # Return the original content as a fallback
        '''
