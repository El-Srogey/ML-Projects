import openai
import streamlit as st
import time


# define the api key 
openai.api_key = ""

# Multi Responses Task
@st.cache
def multi_responses(prompt):
    model = "text-davinci-003"
    response = openai.Completion.create(
      engine=model,
      prompt=prompt,
      max_tokens=1024,
      temperature=0.5,
      stop = None, 
      n = 3,
    )
    responses = []
    responses.append(response["choices"][0]["text"].strip()) # 1st response
    responses.append(response["choices"][1]["text"].strip()) # 2nd response
    responses.append(response["choices"][2]["text"].strip()) # 3rd response 
    return responses

# Machine Translation Task
@st.cache
def machine_trans(sentance, from_lang, to_lang):
    model = "text-davinci-003"
    prompt = f"""The Goal of this prompt is to translate the following sentance from {from_lang} to {to_lang}: {sentance}"""

    response = openai.Completion.create(
      engine=model,
      prompt=prompt,
      max_tokens=len(sentance) + 1024,
      stop = None, 
      n = 1,
      temperature=1
    )

    creative_translation = response["choices"][0]["text"].strip()

    response = openai.Completion.create(
      engine=model,
      prompt=prompt,
      max_tokens=len(sentance) + 1024,
      stop = None, 
      n = 1,
      temperature=0)

    deterministic_translation = response["choices"][0]["text"].strip()
    return creative_translation, deterministic_translation

# Text Summarization Task
@st.cache
def text_sum(text):
    model = "text-davinci-003"
    prompt = f"""Summarize the following paragraph in a creative way: {text}"""

    response = openai.Completion.create(
      engine=model,
      prompt=prompt,
      max_tokens=int(len(text) * .7),
      stop = None, 
      n = 1,
      temperature=1,
    )
    creative_summarization = response["choices"][0]["text"].strip()
   
    prompt = f"""Summarize the following paragraph in a deterministic way: {text}"""
    response = openai.Completion.create(
      engine=model,
      prompt=prompt,
      max_tokens=int(len(text) * .7),
      stop = None, 
      n = 1,
      temperature=0,
    )

    deterministic_summarization = response["choices"][0]["text"].strip()
    return creative_summarization, deterministic_summarization

# Open Conversation Task
# @st.cache
# def open_conv():
#

# Streamlit Part 
st.markdown("## Welcome To Your Own Customized ChatGPT :smiley:")
task_options = ["Machine Translation", "Text Summarization", "One Question, Multi-Responses", "Open Conversation"]
option = st.sidebar.selectbox("Select The Task You Want:", task_options)

st.write("\n")
st.write("\n")


# if MT choseen
if option == task_options[0]:
    languages = ["English", "Arabic", "French", "German", "Italian", "Spanish", "Chinees"]
    from_lang = st.selectbox("Translate From:", languages)
    to_lang = st.selectbox("Translate To:", languages)
    st.text_area("Text", key = "text1")
    try:
        if len(st.session_state.text1) > 0 and st.button("Translate"):
            creative_translation, deterministic_translation = machine_trans(st.session_state.text1.strip(), from_lang, to_lang)
            st.markdown(f'''1. __The Creative Translation:__<p style="color:#FF0000;font-size:16px;border-radius:1%;"> 
                         {creative_translation}</p>''', unsafe_allow_html=True)
            st.markdown(f'''2. __The Deterministic Translation:__<p style="color:#FF0000;font-size:16px;border-radius:1%;">      
                            {deterministic_translation}</p>''', unsafe_allow_html=True)
    except:
        st.markdown('__Request Failed :cry:__')
        
# if Text-SUM choseen    
elif option == task_options[1]:
    st.markdown('Summarize your text in both __Creative__ and __Deterministics__ ways :sparkles:')
    st.text_area('Text', key="text2")
    if len(st.session_state.text2) > 0 and st.button("Summarize"):
        try:
            creative_sum, deterministic_sum = text_sum(st.session_state.text2.strip())
            st.markdown(f'''1. __The Creative Summarization:__<p style="color:#FF0000;font-size:16px;border-radius:1%;"> 
                         {creative_sum}</p>''', unsafe_allow_html=True)
            st.markdown(f'''2. __The Deterministic Summarization:__<p style="color:#FF0000;font-size:16px;border-radius:1%;">      
                            {deterministic_sum}</p>''', unsafe_allow_html=True)
        except:
            st.markdown('__Request Failed :cry:__')
elif option == task_options[2]:
    st.markdown('Enter your prompt and get __Multi-Responses__ :sparkles:')
    st.text_area('Text', key="text3")
    if len(st.session_state.text3) > 0 and st.button("Respond"):
        try:
            responses = multi_responses(st.session_state.text3.strip())
            for i, r in enumerate(responses):
                st.markdown(f"""__{i+1}th response__: <p style="color:#FF0000;font-size:16px;border-radius:1%;">      
                            {responses[i]}</p>""", unsafe_allow_html=True)
        except:
            st.markdown('__Request Failed :cry:__')
else:
    st.markdown("##### Enjoy an Open Conversation Like ChatGPT :smiley:, __Still Under Construction__ :construction:")
    # Define the initial context
    session_state = st.session_state
    if 'context' not in session_state:
        session_state['context'] = ""

    # Define the prompt for the model
    st.write("Enter Your Prompt:")
    user_input = st.text_input("Prompt", "")
    prompt = f"""This conversation context is {session_state['context']}.
                 user's current prompt: {user_input}"""

    # Add a button to submit the prompt
    if st.button("Submit"):
        # Generate a response from the model
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Store the generated text
        global generated_text
        generated_text = response["choices"][0]["text"]
        st.write("ChatGPT: ", generated_text.strip())

        # Update the context with the generated text
        session_state['context'] = session_state['context'] + generated_text

        st.write("Context: ", session_state['context'])
        

# st.markdown("__Enjoy an Open Conversation Like ChatGPT__ :sparkles:'")
# # Define the initial context
# context = ""
#
# # Define the prompt for the model
# user_input = input("")
# prompt = f"""This conversation context is {context}.
#                  user's current prompt: {user_input}"""
#
# while True:
#     # Generate a response from the model
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens= len(user_input) + 1024,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#
#     # Store the generated text
#     generated_text = response["choices"][0]["text"]
#     print("ChatGPT:", generated_text.strip())
#
#     # Update the context with the generated text
#     context = context + generated_text
#
#     # Ask for input from the user
#     print("Enter Your Prompt: ", end="")
#     user_input = input()
#
#     # Update the prompt for the next iteration
#     prompt = f"""This conversation context is {context}.
#                      user's current prompt: {user_input}"""
#
