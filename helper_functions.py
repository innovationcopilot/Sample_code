import openai
import streamlit as st

def generate_response(prompt, history, model_name, temperature):
      # Get the last message sent by the chatbot
      chatbot_message = history[-1]['content']

      # Extract the user's initial message from history
      first_message = history[1]['content']
    
      full_prompt = f"{prompt}\n\
      ### The original message: {first_message}. \n\
      ### Your latest message to me: {chatbot_message}. \n\
      ### Previous conversation history for context: {history}"
      
      # relevant_info = index.query()
      # full_prompt += f"\n### Relevant data from documents: {relevant_info}"
      
      response = openai.ChatCompletion.create(
        model=model_name,
        temperature=temperature,
        messages=[
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": prompt},
        ]
      )
      full_response = ""
      for response in response:
            if 'content' in response['choices'][0]['delta']:
                  full_response += response['choices'][0]['delta']['content']
      yield {"type": "response", "content": full_response}


#################################################################################
# Additional, specific functions I had in the Innovation CoPilot for inspiration:

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

# Function to generate the summary; used in part of the response
def generate_summary(model_name, temperature, summary_prompt):
    summary_response = openai.ChatCompletion.create(
        model=model_name,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "You are an expert at summarizing information effectively and making others feel understood"},
            {"role": "user", "content": summary_prompt},
        ]
    )
    summary = summary_response['choices'][0]['message']['content']
    print(f"summary: {summary}, model name: {model_name}, temperature: {temperature})")
    return summary

# Function used to enable 'summary' mode in wihch the CoPilot only response with bullet points rather than paragraphs
def transform_bullets(content):
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

# Function to add relevant stage specific context into prompt
def get_stage_prompt(stage):
      #Implementation dependent on your chatbots context
      return

# Function to grade the response based on length, relevancy, and depth of response
def grade_response(user_input, assistant_message, idea):
      #Implementation dependent on your chatbots context
      return      

# Function used to generate a final 'report' at the end of the conversation, summarizing the convo and providing a final recomendation
def generate_validation_report():
      #Implementation dependent on your chatbots context
      return
