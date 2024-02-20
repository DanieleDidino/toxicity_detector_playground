<h1 align="center">Chat Safeguard</h1>

<p align="center">A System for Monitoring and Improving Online Language</p>

<p align="center">
<img src=".streamlit/image_1.png" alt="drawing" width="400"/>
</p>

Thank you for your interest in our project. Please be aware that this is only a Proof of Concept system and may contain bugs or unfinished features.

This project aims to develop tools that can detect toxic language in chat conversations and provide suggestions to make the language more respectful and inclusive.

*ADD HERE MORE INFO*

## Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://toxicitydetectorplayground-lvw8o7nmowk5hrmssbvm5y.streamlit.app/)

You will need an <b>OpenAI API key</b> (you can create one [here](https://platform.openai.com/account/api-keys)).

How to use it:
1. Enter your <b>OpenAI API key</b>.
2. Select a Large Language Model ("<b>gpt-3.5-turbo</b>" or "<b>gpt-4</b>").
3. Select whether you want to convert your sentence to a more neutral version ("<i>Convert the sentence to neutral language?</i>" toggle).
4. Enter a sentence to evaluate

The response includes:
1. A label:
   - <b>criticism</b>: This style involves ad hominem attacks on a partner's character rather than addressing specific issues distinguishing it from a complaint, which targets a specific behavior.
   - <b>contempt</b>: An extreme form of criticism, characterized by treating a partner with disrespect, sarcasm, and mockery, making them feel despised and worthless.
   - <b>defensiveness</b>: A response to criticism where one attempts to excuse their behavior and avoid taking responsibility, often resulting in blame-shifting.
   - <b>stonewalling</b>: It occurs when one partner withdraws from the interaction, shutting down communication in response to contempt.
   - <b>neutral</b>: This category is used for text that does not exhibit negative communication patterns nor explicitly fits into the categories of criticism, contempt, defensiveness, or stonewalling. It includes statements or behaviors that are constructive, positive, or at least not harmful or negative in the context of a relationship. Use this category for communication that is understanding, supportive, factual without emotional charge, or otherwise not indicative of conflict. 
   - <b>unclear</b>: Text does not clearly fit into any of the above categories or if it is ambiguous.

2. The token usage.
3. A suggested correction (if the sentence is classified as toxic and the "<i>Convert the sentence to neutral language?</i>" toggle is on).

## Installation

#### Python version: 3.10.12

1. Clone the repo:

    ```bash
    git clone https://github.com/DanieleDidino/toxicity_detector_playground.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
   
3. Run the app in terminal:
   
    ```bash
    streamlit run streamlit_app.py
    ```
