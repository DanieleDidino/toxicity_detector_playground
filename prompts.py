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


def create_prompt_edit_text(label):
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


def create_prompt_split_clf(user_text):
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to split the text into chunks and classify them based on the categories described in the f-string below.

    Args: user_text (str): Text to split and classify.

    Returns:
        A prompt
    """

    prompt = f"""
    Objective: Split the provided text into chunks based on the following categories: 
    'criticism', 'contempt', 'defensiveness', 'stonewalling', 'neutral'.
    If a text chunk does not belong to any specified category, classify it as "other."
    
    Categories Defined:
    
        1. 'criticism': This style involves ad hominem attacks on a partner's character rather than addressing specific issues, distinguishing it from a complaint, which targets a specific behavior.
        2. 'contempt': An extreme form of criticism, characterized by treating a partner with disrespect, sarcasm, and mockery, making them feel despised and worthless.
        3. 'defensiveness': A response to criticism where one attempts to excuse their behavior and avoid taking responsibility, often resulting in blame-shifting.
        4. 'stonewalling': It occurs when one partner withdraws from the interaction, shutting down communication in response to contempt.
        5. 'neutral': This category is used for text that does not exhibit negative communication patterns nor explicitly fits into the categories of criticism, contempt, defensiveness, or stonewalling.
            It includes statements or behaviors that are constructive, positive, or at least not harmful or negative in the context of a relationship.
            Use this category for communication that is understanding, supportive, factual without emotional charge, or otherwise not indicative of conflict.
        6. 'unclear': Use this category if the text does not clearly fit into any of the above categories or if it is ambiguous.
    
    Instructions:
    
        1. Read the text thoroughly.
        2. Identify and extract chunks of text that belong to the specified categories.
        3. Label each chunk with the corresponding category name.
        4. If a text chunk does not fit any of the specified categories, label it as "Other."
        5. Present the categorized text chunks in the following format:
    
    Format:
    
        Category: [Category Name]
        Text: [Extracted Text Chunk]
    
        Category: [Category Name/Other]
        Text: [Extracted Text Chunk]
    
    (Repeat this format for each identified chunk.)
    
    Example:
    
    Given Text: "Why would I do that to you? Are you seriously blaming me for everything? I understand your feelings, and I'm sorry for causing you pain. Maybe you should take a look at your own actions before pointing fingers at me! Let me explain the reasons behind my actions so we can better understand each other."
    
    Expected Output:
    
    Category: criticism
    Text: Why would I do that to you? Are you seriously blaming me for everything?
    
    Category: neutral
    Text: I understand your feelings, and I'm sorry for causing you pain.
    
    Category: criticism
    Text: Maybe you should take a look at your own actions before pointing fingers at me!
    
    Category: neutral
    Text: Let me explain the reasons behind my actions so we can better understand each other.
    
    Please proceed with categorizing the following text:
    
    {user_text}
    """

    return prompt
