from prompt_generation import *
from api_key import get_api_key
from load_environmental_distributions import load_environmental_distribution

import openai

from openai import OpenAI

# import backoff library to handle exponential exceptions
import backoff

import time

import re

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

import json

import matplotlib.pyplot as plt

from textwrap import wrap

@backoff.on_exception(backoff.expo, openai.RateLimitError)
def send_prompt_to_model(question, potential_answers, wave_number, by_group, *args):
    """
    Sends generated prompts to a language model and handles the model's response.

    Args:
        question (str): The question to be sent to the language model.
        potential_answers (list): A list of potential answers to the question.
        wave_number (int): The wave number of the UKHLS study.
        by_group (int): An integer value to determine if the function is simulating synthetic responses by group and which group is the function is testing for.

    Returns:
        response (openai.ChatCompletion): The response from the language model.
        system_prompt (str): The system prompt used for the interaction containing detail about the synthetic individual's profile.

    Raises:
        openai.error.RateLimitError: If the API rate limit is exceeded.
        openai.error.OpenAIError: If there is an error with the OpenAI API.
    """

    if args:
        group = args[0]

        if len(args) > 1:

            is_conditioning = args[1]

            if is_conditioning:    
                system_prompts, user_prompts = get_system_and_user_prompts(question, potential_answers, wave_number, by_group, group, is_conditioning)
            else:
                system_prompts, user_prompts = get_system_and_user_prompts(question, potential_answers, wave_number, by_group, group)
    else:
        system_prompts, user_prompts = get_system_and_user_prompts(question, potential_answers, wave_number, by_group)

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

    response, system_prompt = send_prompt_to_model(test_question, test_potential_answers, test_wave_number, 0)

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

def simulate_synthetic_responses(question, pot_responses, wave_number, by_group, n_samples = 10, *args):
    """
    Description: A function to simulate synthetic responses to the question "Is climate change beyond control" based on the user's profile.

    Parameters:
    •	‘question’ (string): the question to be answered by the LLM.
    •	‘pot_responses’ (list): a list of potential responses for the question.
    •	‘wave_number’ (int): the wave number of the UKHLS study.
    •	‘by_group’ (int): an integer value to determine if the function is simulating synthetic responses by group and which group is the function is testing for.
    •	‘n_samples’ (int): the number of synthetic responses to be generated.

    Returns:
    •	A list of synthetic responses to the question "Is climate change beyond control" based on the user's profile.
    """

    # initialise a variable to store the synthetic responses
    synthetic_responses = []

    for i in range(n_samples):

        if args:
            group = args[0] # determines which group to simulate the responses for
            # check if conditioning information is used to fine-tune the responses. 
            # check the size of the args tuple to determine if the group is used to fine-tune the responses.
            if len(args) > 1:
                is_conditioning = args[1] # the second optional argument is used to determine if conditioning information is used to fine-tune the responses.
                response, user_prompt = send_prompt_to_model(question, pot_responses, wave_number, by_group, group, is_conditioning)
            else:
                response, user_prompt = send_prompt_to_model(question, pot_responses, wave_number, by_group, group)
        else:
        
            response, user_prompt = send_prompt_to_model(question, pot_responses, wave_number, by_group)

        synthetic_responses.append((user_prompt, response)) # append the synthetic response to the list of synthetic responses

    synthetic_responses = extract_synthetic_responses(synthetic_responses, pot_responses)

    return synthetic_responses

def count_responses(filename):
    """
    Count the total number of responses in a JSON file.

    Parameters:
    filename (str): The path to the JSON file.

    Returns:
    int: The total number of responses.
    """
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    total_responses = 0
    # Iterate through each question's responses
    for item in data:
        # Iterate through the synthetic responses dictionary and sum the values
        responses = item['Synthetic Responses']
        total_responses += sum(responses.values())
    
    return total_responses

def visualise_synthetic_and_ukhls_distributions(file_name, question, question_number, distribution, wave_number):
    '''
    Description: A function to visualise the synthetic and UKHLS distributions of the responses to a question.

    Parameters:
    • 'file_name' (str): The name of the JSON file containing the synthetic responses.
    • 'question' (str): The question to which the responses belong.
    • 'question_number' (int): The question number.
    • 'distribution' (dict): The distribution of responses to the question in the UKHLS data in a numpy array format. 
    • 'wave_number' (int): The wave number of the UKHLS data.

    Returns:
    None - this function plots the synthetic and UKHLS distributions in the same plot using different colours. 
    '''
    if question_number == 1:
        # initialise the ordered response categories for question 0: demo question 
        ordered_categories = ["Don't do Anything Environmentally Friendly", "Do One or Two Things Environmentally Friendly", "Do Some Things Environmentally Friendly", "Do Many Things Environmentally Friendly", "Do Everything Environmentally Friendly"]
    elif question_number == 2:
        ordered_categories = ['Entirely Positive', 'More Positive than Negative', 'Neither', 'More Negative than Positive', 'Entirely Negative']
    elif question_number == 3 or question_number == 4 or question_number == 6 or question_number == 10:
        ordered_categories = ["Strongly Agree", "Tend to Agree", "Neither", "Tend to Disagree", "Strongly Disagree"]
    elif question_number == 5: 
        ordered_categories = ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree", "Already Changed"]
    elif question_number == 7:
        ordered_categories = ["Yes - already buy", "Yes - seriously considering", "No", "Considered and rejected"]
    elif question_number == 8:
        ordered_categories = ["Yes", "No"]
    elif question_number == 9:
        ordered_categories = ["Mentioned", "Not Mentioned"]
    else:
        ordered_categories = [] # exception handling for unknown questions. 

    # convert ordered_categories to lower case
    ordered_categories = [category.lower() for category in ordered_categories]
            
    # Load the synthetic responses from the JSON file
    with open(file_name, "r") as file:
        synthetic_responses = json.load(file)

    # extract the synthetic responses into a dictionary
    aggregated_synthetic_responses = {}

    # iterate through the synthetic responses
    for entry in synthetic_responses:
        if entry["Question"] == question:
            
            for response, count in entry["Synthetic Responses"].items():

                # convert response to lower case
                response = response.lower()

                if response in aggregated_synthetic_responses:
                    aggregated_synthetic_responses[response] += count
                else:
                    aggregated_synthetic_responses[response] = count

    # implement a code to iterate through the ordered categories to check if they are in the synthetic responses
    for category in ordered_categories:

        if category not in aggregated_synthetic_responses:
            aggregated_synthetic_responses[category] = 0

    # sort the synthetic responses in the order of the ordered categories
    aggregated_synthetic_responses = {key: aggregated_synthetic_responses[key] for key in ordered_categories} 

    # convert distribution to a dictionary structure format
    distribution_dict = {str(key): value for key, value in distribution.items()}

    # convert every key in distribution variable to lower-case
    distribution_dict = {key.lower(): value for key, value in distribution_dict.items()}

    # sort distribution dictionary in the order of the ordered categories
    distribution_dict = {key: distribution_dict[key] for key in ordered_categories}

    # check distributions of aggregated synthetic responses and distribution_dict
    # print("Aggregated Synthetic Responses: ", aggregated_synthetic_responses)
    # print("Distribution Dictionary: ", distribution_dict)

    x = range(len(ordered_categories))  # label locations
    width = 0.35  # width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, aggregated_synthetic_responses.values(), width, label='Synthetic', color='blue')
    rects2 = ax.bar([p + width for p in x], distribution_dict.values(), width, label='UKHLS', color='red')

    ax.set_ylabel('Frequency') # set the y-axis label

    if question_number == 2:
        ax.set_title(f'Responses to Question {question_number}') # set the title of the plot
    else:
        ax.set_title(f'Responses to Question {question_number} in Wave {wave_number}') # set the title of the plot
    ax.set_xticks([p + width / 2 for p in x]) # set the x-axis ticks

    # format the ordered_categories to be in title case
    ordered_categories = ['\n'.join(wrap(l, 12)) for l in ordered_categories]

    ax.set_xticklabels(ordered_categories, rotation=90, fontsize=8) # set the x-axis labels
    ax.legend() # display the legend

    # save the figure as a png file
    plt.savefig(f"C:\\Users\\haoch\\Documents\\COMP0190\\Data\\COMP0191-MSc-Project-Code\\Figures\\Synthetic-UKHLS-Comparisons\\Question {question_number} Wave {wave_number}.png", bbox_inches='tight')

    plt.show() # display the plot

def write_responses_to_json(question, new_responses, filename):
    """
    Description: A function to append synthetic responses related to a question to a JSON file without overwriting existing content, 
    using a list to support multiple entries including potentially identical questions.

    Parameters:
    • 'question' (str): The question to which the responses belong.
    • 'new_responses' (dict): A dictionary of synthetic responses.
    • 'filename' (string): The name of the JSON file to write the responses to.

    Returns:
    • A JSON file containing the updated responses.
    """

    # Load existing data or initialize an empty list if the file doesn't exist or is empty
    try:
        with open(filename, "r") as file:
            existing_responses = json.load(file)
            if not isinstance(existing_responses, list):
                raise ValueError("The existing JSON content is not a list.")
    except (FileNotFoundError, json.JSONDecodeError):
        existing_responses = []

    # Create a new entry for the response
    response_entry = {
        "Question": question,
        "Synthetic Responses": new_responses
    }

    # Append the new entry to the list
    existing_responses.append(response_entry)

    # Write the updated list back to the JSON file
    with open(filename, "w") as file:
        json.dump(existing_responses, file, indent=4)

def simulate_environmental_responses(question, question_number, potential_answers, n_samples, json_filepath, distributions, wave_numbers, wave_number, is_simulate, by_group, *args):

    '''
    Description: A function to simulate synthetic responses to specific questions about environmental issues.

    Parameters:
    • question (str): the question to be answered by the LLM.
    • potential_answers (list): a list of potential responses for the question.
    • n_samples (int): the number of synthetic responses to be generated.
    • json_filepath (str): the path to the JSON file containing the synthetic responses.
    • distributions (dict): a dictionary containing the probability distributions of the UKHLS environmental views context.
    • is_simulate (bool): a boolean value to determine if the function should simulate synthetic responses or not. (default is True
    • by_group (int): an integer value to determine if the function is simulating synthetic responses by group and which group is the function is testing for. (default is 0)

    Returns:
    None
    '''
    sample_size = count_responses(json_filepath) # get the total number of responses in the JSON file

    print(f"Sample size: {sample_size}")

    if is_simulate:

        if args:

            group = args[0] # determines which group to simulate the responses for

            responses = simulate_synthetic_responses(question, potential_answers, wave_number, by_group, n_samples, group)

        else:

            responses = simulate_synthetic_responses(question, potential_answers, wave_number, by_group, n_samples) # simulate synthetic responses

        sample_size += n_samples # update the sample size with the new responses

        write_responses_to_json(question, responses, json_filepath) # write the synthetic responses to the JSON file

    if by_group == 0:

        for distribution, wave_number in zip(distributions, wave_numbers):
            # iterate through each ukhls distribution for comparing with the synthetic responses. 
            
            distribution = {key: round(value * sample_size) for key, value in distribution.items()}

            # test display the distribution data to check if the values are correct
            # print(f"Wave {wave_number} Distribution: {distribution}")

            visualise_synthetic_and_ukhls_distributions(json_filepath, question, question_number, distribution, wave_number)

def test_simulate_synthetic_responses_function():
    """
    Test function for the simulate_synthetic_responses function.
    """
    test_question = "To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?"
    test_potential_answers = ["Strongly agree", "Tend to agree", "Neither agree nor disagree", "Tend to disagree", "Strongly disagree"]
    test_wave_number = 1

    synthetic_responses = simulate_synthetic_responses(test_question, test_potential_answers, test_wave_number, 1, 10, "18 - 34")

    # display the synthetic responses
    print(synthetic_responses)

    assert len(synthetic_responses) == 5

    print("test_simulate_synthetic_responses_function PASSED")

# test_simulate_synthetic_responses_function()