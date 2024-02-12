from openai import OpenAI
import streamlit as st
from utils import create_prompt_template

####################################################################################
# Config

# About text for the menu item
about = """
This app is a playground to experiment with LLM to detect toxic/violent language and convert it to neutral text
"""

# streamlit config
st.set_page_config(
    page_title="ToxLang Playground",
    layout="wide",
    menu_items={
        "About": about
    }
)

st.header("Enter a sentence to evaluate")

# Condense the layout
padding = 0
st.markdown(
    f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """,
    unsafe_allow_html=True,
)

# load custom css styles
with open(".streamlit/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Dictionary for LLM selection
llm_available = {
    "Open AI: gpt-3.5-turbo":"gpt-3.5-turbo",
    "Open AI: gpt-4": "gpt-4",
}

# LLM temperature
TEMPERATURE = 0

# System content for classifying toxic language
system_content_clf = create_prompt_template()

# System content for converting toxic language into neutral language
system_content_edit = f"""
You are an expert non-violent comunication.
I will show you an example of toxic language,
your task is to modify the text into a neutral version.
Try to maintain the original meaning.
"""

####################################################################################
# Left column

sidebar = st.sidebar

with sidebar:

    # Custom page title and subtitle
    st.title("ToxLang")
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Detect and correct toxic language", divider="orange")
    st.markdown("<br>", unsafe_allow_html=True)

    # Get OpenAI ley from user
    openai_label = "Enter your [OpenAi key](https://platform.openai.com/account/api-keys)"
    OPENAI_KEY = st.text_input(label=openai_label, type="password", help="Enter your OpenAi key")

    # Add space between elements of the column
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Selectbox with the list of LLM
    help_selectbox_llm = "This option is for when we will use open-source LLM"
    selected_llm = st.selectbox("Select a LLM", options=llm_available.keys(), help=help_selectbox_llm)
    if selected_llm and OPENAI_KEY:
        LLM_MODEL = llm_available[selected_llm]
        # Initialize LLM
        if "client_openai" not in st.session_state:
            st.session_state.client_openai = OpenAI(api_key=OPENAI_KEY)
    
    # Add space between elements of the column
    st.markdown("<br>", unsafe_allow_html=True)

    # Initialize edit_text (define whether or not convert the toxic to neutral language)
    if "edit_text" not in st.session_state:
        st.session_state.edit_text = False
    
    # Toggle to select whether convert the original text
    help_toggle_edit_text = "Conver the sentence to neutral language?"
    st.session_state.edit_text = st.toggle("Convert to neutral language?", value=False, help=help_toggle_edit_text)

####################################################################################
# Chat

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)
    
# React to user input
if prompt := st.chat_input("How may I help you?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if OPENAI_KEY:
        # Detect toxic language
        completion = st.session_state.client_openai.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_content_clf},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
        )
        selected_label = completion.choices[0].message.content
        completion_tokens = completion.usage.completion_tokens
        prompt_tokens = completion.usage.prompt_tokens
        total_tokens = completion.usage.total_tokens
        # Edit text
        if st.session_state.edit_text and selected_label!="unclear" and selected_label!="neutral":
            completion = st.session_state.client_openai.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_content_edit},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
            )
            edited_text = completion.choices[0].message.content
            edited_text = f"<br><br>Suggested correction:<br><font style='background-color: #FFFF00'>{edited_text}</font>"
            completion_tokens += completion.usage.completion_tokens
            prompt_tokens += completion.usage.prompt_tokens
            total_tokens += completion.usage.total_tokens
        else:
            edited_text = ""
        # Prepare response for user
        used_tokens = {
            "completion_tokens":completion_tokens,
            "prompt_tokens":prompt_tokens,
            "total_tokens":total_tokens
        }
        if st.session_state.edit_text:
            response_for_user = f"This sentence is labeled as <b style='color: red'>{selected_label}</b><br>(token usage: {used_tokens}){edited_text}"

            
    else:
        response_for_user = "Please add your OpenAI key to continue."

    # Display response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_for_user, unsafe_allow_html=True)
    # Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_for_user})
