import environ
from openai import OpenAI
import openai
from pathlib import Path
import pandas as pd
from functools import partial
from typing import Callable
from datetime import datetime

from utils import get_responses_from_llm

# README:
# This script classifies text and transform it into a more functional version.
# It loads and uses the text in the folder "example_text".

def load_data(path_load_data):
    data = pd.read_csv(path_load_data)
    data_melt = pd.melt(
        data,
        id_vars=['communication_style'],
        var_name='user_type',
        value_name='text')
    return data_melt


def call_api(
        data: pd.DataFrame,
        api_client:openai.OpenAI,
        llm_model: str,
        temperature: float,
        fnc_get_responses: Callable[[str, openai.OpenAI, str, float], tuple],
        ) -> tuple:
    
    if not callable(fnc_get_responses):
        raise ValueError("fnc_get_responses must be a callable.")

    # Set all parameters but "user_text"
    partial_fnc_get_responses = partial(
        fnc_get_responses,
        api_client=api_client,
        llm_model=llm_model,
        temperature=temperature
    )

    clf_text = []
    edited_text = []

    for i in range(data.shape[0]):
        clf_text_tmp, edited_text_tmp, _ = partial_fnc_get_responses(user_text=data.text[i])
        clf_text.append(clf_text_tmp)
        edited_text.append(edited_text_tmp)
        if (i % 5) == 0:
            print(f"Done index {i} of {data.shape[0]}")
    
    return clf_text, edited_text


def add_columns(data: pd.DataFrame, clf_text: list[str], edited_text: list[str]) -> pd.DataFrame:

    # Remove leading newline characters and replace "\n    " with "\n"
    clf_text = [s.lstrip() for s in clf_text]
    clf_text = [s.replace('\n    ', '\n') for s in clf_text]
    edited_text = [s.lstrip() for s in edited_text]
    edited_text = [s.replace('\n    ', '\n') for s in edited_text]

    # Add columns with "clf_text" and "edited_text"
    data["clf_text"] = clf_text
    data["edited_text"] = edited_text

    return data


def main():
    # Import OpenAI key
    env = environ.Env()
    environ.Env.read_env()
    OPENAI_API_KEY = env("OPENAI_API_KEY")
    
    # Set constanst
    LLM_MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0
    API_CLIENT = OpenAI(api_key=OPENAI_API_KEY)
    print(f"Using {LLM_MODEL}, with temperature={TEMPERATURE}")
    
    # Set paths
    path_load_data = Path("./example_text", "examples_com_style.csv")
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"clf_examples_{datetime_str}.csv"
    path_save_data = Path("./example_text", file_name)

    # load data
    print(f"Loading data from: {path_load_data}")
    data = load_data(path_load_data)

    # Call OpenAI API
    print("Start classifying text")
    clf_text, edited_text = call_api(
        data=data,
        api_client=API_CLIENT,
        llm_model=LLM_MODEL,
        temperature=TEMPERATURE,
        fnc_get_responses=get_responses_from_llm)
    print("Done classifying text")


    data_to_print = add_columns(data, clf_text, edited_text)
    
    # Save to csv
    print(f"Saving data to: {path_save_data}")
    data_to_print.to_csv(path_save_data)


# The following condition checks if this script is being run directly
if __name__ == "__main__":

    main()    
