def create_prompt_clf():
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to categorize the text.

    Args: None

    Returns:
        A prompt
    """

    prompt = (
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
        
        Your objective is to generate a label that classifies the provided text according to these categories.
        As answer only provide the predicted label and nothing else.
        Here is the text for classification:
        """
    )
    return prompt


def create_prompt_edit(label):
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to edit the text to covert it in a more functional version.

    Args: label (str): a label that classify the text, possible lalbels:
          criticism, contempt, defensiveness, stonewalling, neutral, unclear

    Returns:
        A prompt
    """

    prompt = f"""
    You are an expert in conflict resolution and effective communication strategies, with a focus on the four communication styles identified by Dr. John Gottman.
    The text below was classified as {label}.
    Your task is to modify the text to create a more neutral functional text.
    Try to maintain the original meaning.
    """
    return prompt
