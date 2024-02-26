from openai import OpenAI
import streamlit as st
from utils import get_responses_from_llm

####################################################################################
# Config

# About text for the menu item
about = """
This app is a playground to experiment with LLM to detect disfunctional language and convert it to functional text.
"""

# streamlit config
st.set_page_config(
    page_title="D-AI-logue",
    layout="wide",
    menu_items={
        "About": about
    }
)

st.header("Enter text to evaluate")

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

text_area_hight =500

# Initialize parameters
default_values = {
   "messages": [],
   "avatars": [],
   "text_user1": "",
   "text_user2": "",
   "clf_user1": "",
   "clf_user2": "",
   "edited_text_user1": "",
   "edited_text_user2": "",
   "total_token_user1": 0,
   "total_token_user2": 0,
   "use_original_text_user1": False,
   "use_original_text_user2": False,
   "use_edited_text_user1": False,
   "use_edited_text_user2":False,
}

# Set the default value in session_state if not already set
for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

####################################################################################
# Left column

with st.sidebar:

    # Custom page title and subtitle
    st.title("D-AI-logue")
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("", divider="orange") # Improve personal communication
    st.markdown("<br>", unsafe_allow_html=True)

    # Get OpenAI ley from user
    openai_label = ":key: Enter your [OpenAi key](https://platform.openai.com/account/api-keys)"
    OPENAI_KEY = st.text_input(label=openai_label, type="password", help="Enter your OpenAi key")

    # Add space between elements of the column
    st.markdown("<br>", unsafe_allow_html=True)

    # Selectbox with the list of LLM
    help_selectbox_llm = "This option is for when we will use open-source LLM"
    selected_llm = st.selectbox("Select a LLM", options=llm_available.keys(), help=help_selectbox_llm)
    if selected_llm and OPENAI_KEY:
        llm_model = llm_available[selected_llm]
        # Initialize LLM
        if "client" not in st.session_state:
            st.session_state.client = OpenAI(api_key=OPENAI_KEY)
    
    # Add space between elements of the column
    st.markdown("<br>", unsafe_allow_html=True)

####################################################################################
# Main 

# Set 3 columns for first row (user 1)
col1_row1, col2_row1, col3_row1 = st.columns(3)

# Set column 1 - row 1 (user 1)
with col1_row1:
    st.session_state.text_user1 = st.text_area(label = "User 1:", value=st.session_state.text_user1, help="Text from user 1", height=text_area_hight)
    button_go_user1, text_token_usage_user1 = st.columns(2)
    with button_go_user1:
        go_btn_user1 = st.button("Go...", key="go_user1")

# Set 3 columns for second row (user 2)
col1_row2, col2_row2, col3_row2 = st.columns(3)

# Set column 1 - row 2 (user 2)
with col1_row2:
    st.session_state.text_user2 = st.text_area(label = "User 2:", value=st.session_state.text_user2, help="Text from user 2", height=text_area_hight)
    button_go_user2, text_token_usage_user2 = st.columns(2)
    with button_go_user2:
        go_btn_user2 = st.button("Go...", key="go_user2")

# React to user 1 input
if go_btn_user1:
    if OPENAI_KEY:
        clf_text_user1, edited_text_user1, total_token = get_responses_from_llm(
            user_text=st.session_state.text_user1,
            api_client=st.session_state.client,
            llm_model=llm_model,
            temperature=TEMPERATURE
        )
        st.session_state.clf_user1 = clf_text_user1
        st.session_state.edited_text_user1 = edited_text_user1
        st.session_state.total_token_user1 = total_token
    else:
        st.session_state.clf_user1 = "Please add your OpenAI key to continue."
        st.session_state.edited_text_user1 = "Please add your OpenAI key to continue."
        st.session_state.total_token_user1 = 0

# React to user 2 input
if go_btn_user2:
    if OPENAI_KEY:
        clf_text_user2, edited_text_user2, total_token = get_responses_from_llm(
            user_text=st.session_state.text_user2,
            api_client=st.session_state.client,
            llm_model=llm_model,
            temperature=TEMPERATURE
        )
        st.session_state.clf_user2 = clf_text_user2
        st.session_state.edited_text_user2 = edited_text_user2
        st.session_state.total_token_user2 = total_token
    else:
        st.session_state.clf_user2 = "Please add your OpenAI key to continue."
        st.session_state.edited_text_user2 = "Please add your OpenAI key to continue."
        st.session_state.total_token_user2 = 0

# Set columns 2 and 3 - row 1 (user 1)
col2_clf_user_1 = col2_row1.text_area(label = "Classification 1", value=st.session_state.clf_user1, height=text_area_hight)
col3_edt_user_1 = col3_row1.text_area(label = "Suggested text 1", value=st.session_state.edited_text_user1, height=text_area_hight)

# Set columns 2 and 3 - row 2 (user 2)
col2_clf_user_2 = col2_row2.text_area(label = "Classification 2", value=st.session_state.clf_user2, height=text_area_hight)
col3_edt_user_2 = col3_row2.text_area(label = "Suggested text 2", value=st.session_state.edited_text_user2, height=text_area_hight)

# Set buttons in column 3 - row 1 (user 1)
with col3_row1:
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        st.session_state.use_original_text_user1 = st.button("Use original text", key="use_original_usr1")
    with button_col2:
        st.session_state.use_edited_text_user1 = st.button("Use modified text", key="use_modified_usr1")

# If "Use original text" or "Use modified text" button pressed, add text and avatar to chat history (user 1)
if st.session_state.use_edited_text_user1:
    st.session_state.messages.insert(0, {"role": "assistant", "content": st.session_state.edited_text_user1})
    st.session_state.avatars.insert(0, "👩‍🦰")
    # st.session_state.use_edited_text_user1 = False
elif st.session_state.use_original_text_user1:
    st.session_state.messages.insert(0, {"role": "assistant", "content": st.session_state.text_user1})
    st.session_state.avatars.insert(0, "👩‍🦰")
    # st.session_state.use_original_text_user1 = False

# Add token usage to column 1 - row 1 (user1)
with text_token_usage_user1:
    st.write(f"token usage: {st.session_state.total_token_user1}")

# Add token usage to column 1 - row 2 (user2)
with text_token_usage_user2:
    st.write(f"token usage: {st.session_state.total_token_user2}")

# Set buttons in column 3 - row 1 (user 1)
with col3_row2:
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        st.session_state.use_original_text_user2 = st.button("Use original text", key="use_original_usr2")
    with button_col2:
        st.session_state.use_edited_text_user2 = st.button("Use modified text", key="use_modified_usr2")

# If "Use original text" or "Use modified text" button pressed, add text and avatar to chat history (user 2)
if st.session_state.use_edited_text_user2:
    st.session_state.messages.insert(0, {"role": "assistant", "content": st.session_state.edited_text_user2})
    st.session_state.avatars.insert(0, "👨‍🦰")
    # st.session_state.use_edited_text_user2 = False
elif st.session_state.use_original_text_user2:
    st.session_state.messages.insert(0, {"role": "assistant", "content": st.session_state.text_user2})
    st.session_state.avatars.insert(0, "👨‍🦰")
    # st.session_state.use_original_text_user2 = False

# Add "reset chat" button befor the chat history
reset_chat = st.button("Reset chat history?")
if reset_chat:
    st.session_state.messages = []
    st.session_state.avatars = []

# Display chat messages from history on app rerun
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"], avatar=st.session_state.avatars[i]):
        st.markdown(message["content"], unsafe_allow_html=True)
