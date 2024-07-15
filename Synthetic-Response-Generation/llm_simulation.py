from prompt_generation import *
from api_key import get_api_key

import openai

from openai import OpenAI

# import backoff library to handle exponential exceptions
import backoff

import time

import re

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

@backoff.on_exception(backoff.expo, openai.RateLimitError)
def send_prompt_to_model(question, potential_answers, wave_number):
    """
    Sends generated prompts to a language model and handles the model's response.

    Args:
        question (str): The question to be sent to the language model.
        potential_answers (list): A list of potential answers to the question.
        wave_number (int): The wave number of the UKHLS study.

    Returns:
        response (openai.ChatCompletion): The response from the language model.
        system_prompt (str): The system prompt used for the interaction containing detail about the synthetic individual's profile.

    Raises:
        openai.error.RateLimitError: If the API rate limit is exceeded.
        openai.error.OpenAIError: If there is an error with the OpenAI API.
    """
    system_prompts, user_prompts = get_system_and_user_prompts(question, potential_answers, wave_number)

    # define the max_tokens as the maximum length of answers from potential_answers
    max_tokens = max(len(answer) for answer in potential_answers)
    
    # Implement exception handling to process OpenAI API errors. 
    try:
        # Create a chat completion request to the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompts[0]},
                {"role": "user", "content": user_prompts[0]},
                {"role": "system", "content": system_prompts[1]}
            ],
            temperature=0.7, # change the temperature back to 0.7 following argyle 2022 response
            max_tokens=max_tokens  # Adjust max_tokens as needed
        )

        time.sleep(1) # sleep for 1 second to avoid rate limit errors

        # returns the response from the language model and the system prompt containing the synthetic individual's profile
        return response.choices[0].message.content, user_prompts[0]

    except openai.RateLimitError as e:
        # Handle rate limit errors specifically
        print(f"Rate limit error: {e}")
        raise
    except openai.OpenAIError as e:
        # Handle other OpenAI API errors
        print(f"OpenAI API error: {e}")
        return None, None


def test_send_prompt_to_model_function():
    """
    Test function for the send_prompt_to_model function.
    """
    test_question = "To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?"
    test_potential_answers = ["Strongly agree", "Tend to agree", "Neither agree nor disagree", "Tend to disagree", "Strongly disagree"]
    test_wave_number = 13

    api_key = get_api_key()

    client = OpenAI(api_key = api_key)

    response, system_prompt = send_prompt_to_model(test_question, test_potential_answers, test_wave_number)

    print("My response is: ", response)

    assert response is not None
    assert system_prompt is not None

    print("test_send_prompt_to_model_function PASSED")

def extract_synthetic_responses(synthetic_responses, potential_responses):
    """

    Description: A function to extract synthetic responses from the potential responses.

    Parameters:
    •	‘synthetic_responses’ (list): a list of synthetic responses.
    •	‘potential_responses’ (list): a list of potential responses.

    Returns:
    •	A dictionary containing the synthetic responses and their frequency count.
    """
    sythetic_response_tally = {}

    # convert both synthetic responses and potential responses to lowercase to standardize the comparison
    synthetic_responses = [response.lower() for (user_prompt, response) in synthetic_responses]
    potential_responses = [response.lower() for response in potential_responses]

    # remove punctuations from the synthetic responses
    punctuations = r'[^\w\s]'  # This pattern matches anything that is not a word character or whitespace

    synthetic_responses = [re.sub(punctuations, '', response) for response in synthetic_responses]

    for response in synthetic_responses:
        if response in potential_responses: # if the response is present in the potential responses
            # check if the response is in the potential responses
            if response in sythetic_response_tally:
                sythetic_response_tally[response] += 1
            else:
                sythetic_response_tally[response] = 1
        else:
            # check if a substring of the response is in the potential responses
            # print("Response: ", response)

            vectorizer = TfidfVectorizer()

            # fit the vectorizer on the variable "response"
            response_vector = vectorizer.fit_transform([response])

            # fit the vectorizer on the potential responses
            potential_responses_vector = vectorizer.transform(potential_responses)

            # calculate the cosine similarity between the response and the potential responses
            similarity_scores = cosine_similarity(response_vector, potential_responses_vector)

            # get the index of the potential response with the highest similarity score
            most_similar_index = np.argmax(similarity_scores)

            # get the most similar potential response
            most_similar_response = potential_responses[most_similar_index]

            # print("Most Similar Response: ", most_similar_response)

            if most_similar_response in sythetic_response_tally:
                sythetic_response_tally[most_similar_response] += 1
            else:
                sythetic_response_tally[most_similar_response] = 1

    for response in potential_responses: # assigns a frequency of 0 to potential responses that were not generated
        if response not in sythetic_response_tally:
            sythetic_response_tally[response] = 0

    return sythetic_response_tally

def simulate_synthetic_responses(question, pot_responses, wave_number, n_samples = 10):
    """
    Description: A function to simulate synthetic responses to the question "Is climate change beyond control" based on the user's profile.

    Parameters:
    •	‘question’ (string): the question to be answered by the LLM.
    •	‘pot_responses’ (list): a list of potential responses for the question.
    •	‘wave_number’ (int): the wave number of the UKHLS study.
    •	‘n_samples’ (int): the number of synthetic responses to be generated.

    Returns:
    •	A list of synthetic responses to the question "Is climate change beyond control" based on the user's profile.
    """

    # initialise a variable to store the synthetic responses
    synthetic_responses = []

    for i in range(n_samples):
        
        response, user_prompt = send_prompt_to_model(question, pot_responses, wave_number)

        synthetic_responses.append((user_prompt, response)) # append the synthetic response to the list of synthetic responses

    synthetic_responses = extract_synthetic_responses(synthetic_responses, pot_responses)

    return synthetic_responses

def test_simulate_synthetic_responses_function():
    """
    Test function for the simulate_synthetic_responses function.
    """
    test_question = "To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?"
    test_potential_answers = ["Strongly agree", "Tend to agree", "Neither agree nor disagree", "Tend to disagree", "Strongly disagree"]
    test_wave_number = 1

    synthetic_responses = simulate_synthetic_responses(test_question, test_potential_answers, test_wave_number)

    # display the synthetic responses
    print(synthetic_responses)

    assert len(synthetic_responses) == 5

    print("test_simulate_synthetic_responses_function PASSED")

test_simulate_synthetic_responses_function()