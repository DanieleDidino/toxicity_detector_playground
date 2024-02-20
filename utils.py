#from openai import OpenAI
import streamlit as st
from prompts import create_prompt_split_clf, create_prompt_edit_text

def test_label(label):
    """
    Check if the predicted label belongs to the expected categories.

    Args:
        label (string): Label returned by the model

    Returns:
        'True' if the label belongs to the categories; 'False' otherwise.
    """

    if label in ["criticism", "contempt", "defensiveness", "stonewalling", "neutral", "unclear"]:
        return True
    else:
        return False


def call_api_client(api_client, llm_model, system_prompt, user_text, temperature):
    """
    Call the API and get the response.

    Args:
        api_client: Object that manage the call to OpenAI API.
        llm_model (string): Name of the OpenAI model.
        system_prompt (string): A prompt used to inform the model how to modify the user text.
        user_text (string): Original text provided by the user.
        temperature (float): Temperature for the OpenAI model.

    Returns:
        response (string): response from api (a label, edited text, or some text)
        token_usage (tuple): the number of tokens used
    """

    chat_completion = api_client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        temperature=temperature
    )

    response = chat_completion.choices[0].message.content

    token_usage = count_token_usage(chat_completion)

    return response, token_usage


def count_token_usage(api_response):
    """
    Count how many token have been sent to the API.
    This version is specific for OpenAI and Streamlit.

    Args:
        api_response: Object returned by a synchronous openai client instance

    Returns:
        (tuple): the number of tokens used, that is
            - 'completion_tokens': token generated by the model.
            - 'prompt_tokens': tokens sent to the api.
            - 'total_tokens': total count of used tokens.
    """

    completion_tokens = api_response.usage.completion_tokens
    prompt_tokens = api_response.usage.prompt_tokens
    total_tokens = api_response.usage.total_tokens

    return (completion_tokens, prompt_tokens, total_tokens)


def get_responses_from_llm(user_text, api_client, llm_model, temperature):
    """
    This function perform the following steps:
        1) Call a function to create a prompt to split and classify the text.
        2) Call the API with the create prompt to get the text classification.
        3) Call a function to create a prompt to use to edit the text into a more functional version.
        4) Call the API with the second prompt to get the modified functional text.

    Args:
        user_text (string): Original text provided by the user.
        api_client: Object that manage the call to OpenAI API.
        llm_model (string): Name of the OpenAI model.
        temperature (float): Temperature for the OpenAI model.

    Returns:
        A tuple with the following objects:
            - 'clf_text': Text split into chunks and classified into categories.
            - 'edited_text': Text converted in a more functional version.
            - 'total_token': total count of used tokens.
    """

    # Split and classify the text
    prompt_split_clf = create_prompt_split_clf(user_text)
    clf_text, token_usage = call_api_client(
        api_client= api_client,
        llm_model=llm_model,
        system_prompt="",
        user_text=prompt_split_clf,
        temperature=temperature)
            
    # Compute token usage
    _, _, total_token = token_usage

    # Edit the taxt into a more functinal format
    prompt_edit_text = create_prompt_edit_text(clf_text)
    edited_text, token_usage = call_api_client(
        api_client= api_client,
        llm_model=llm_model,
        system_prompt=prompt_edit_text,
        user_text=clf_text,
        temperature=temperature)
    
    # Compute token usage
    _, _, total_token_tmp = token_usage
    total_token += total_token_tmp

    return clf_text, edited_text, total_token

