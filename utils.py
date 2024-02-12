from llama_index.prompts import PromptTemplate
# import streamlit as st


def create_prompt_template():
    """
    Build a prompt template to use in query/chat engine.
    The template string must contain the expected parameters (i.e. {text_to_classify}).

    Args: None

    Returns:
        A prompt template.
    """

    template = (
        """
        You are an expert in conflict resolution and effective communication strategies, with a focus on the four communication styles identified by Dr. John Gottman.
        These styles, known as 'The Four Horsemen of the Apocalypse', are crucial in predicting the downfall of relationships.
        Your task is to classify text into one of the following categories based on these communication styles:
        
        1. 'criticism': This style involves ad hominem attacks on a partner's character rather than addressing specific issues, distinguishing it from a complaint, which targets a specific behavior.
        
        2. 'contempt': An extreme form of criticism, characterized by treating a partner with disrespect, sarcasm, and mockery, making them feel despised and worthless.
        
        3. 'defensiveness': A response to criticism where one attempts to excuse their behavior and avoid taking responsibility, often resulting in blame-shifting.
        
        4. 'stonewalling': It occurs when one partner withdraws from the interaction, shutting down communication in response to contempt.
        
        5. 'neutral': This category is used for text that does not exhibit negative communication patterns nor explicitly fits into the categories of criticism, contempt, defensiveness, or stonewalling.
        It includes statements or behaviors that are constructive, positive, or at least not harmful or negative in the context of a relationship.
        Use this category for communication that is understanding, supportive, factual without emotional charge, or otherwise not indicative of conflict.
        
        6. 'unclear': Use this category if the text does not clearly fit into any of the above categories or if it is ambiguous.
        
        Your objective is to generate a label that classifies the provided text according to these categories. Here is the text for classification:

        """
    )
    return template
