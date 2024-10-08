# import the necessary libraries
import json

import matplotlib.pyplot as plt

from textwrap import wrap

import os

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
    width = 0.15  # width of the bars

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
    plt.savefig(f"Figures/Synthetic-UKHLS-Comparisons/Question {question_number} Wave {wave_number}.png", bbox_inches='tight')

    plt.show() # display the plot

# test the visualise_synthetic_and_ukhls_distributions function
demo_json_filepath = "C:\\Users\\haoch\\Documents\\COMP0190\\Data\\COMP0191-MSc-Project-Code\\Synthetic-Responses-JSON\\synthetic_responses_demo.json"
demo_question = "And which of these would you say best describes your current lifestyle?"
question_number = 1
potential_answers = ["Don't do Anything Environmentally Friendly", "Do One or Two Things Environmentally Friendly", "Do Some Things Environmentally Friendly", "Do Many Things Environmentally Friendly", "Do Everything Environmentally Friendly"]

# Using the formatted path variable
def test_formatted_json_filepath(path):

    if os.path.exists(path):
        with open(path, 'r') as file:
            # Perform operations with the file
            data = file.read()
            print(data)
    else:
        print(f"File not found: {path}")

# test_formatted_json_filepath(demo_json_filepath)

def visualise_responses_by_group(file_names, question):

    synthetic_responses = []

    if question == "Demo":
        ordered_categories = ["Don't do Anything Environmentally Friendly", "Do One or Two Things Environmentally Friendly", "Do Some Things Environmentally Friendly", "Do Many Things Environmentally Friendly", "Do Everything Environmentally Friendly"]
    if question == "Q1":
        print("Question 1")
        ordered_categories = ["Entirely Negative", "More negative than positive", "Neither positive nor negative", "More positive than negative", "Entirely Positive"]
    if question == "Q2":
        ordered_categories = ["Strongly Agree", "Tend to Agree", "Neither", "Tend to Disagree", "Strongly Disagree"]

    # convert ordered_categories to lower case
    ordered_categories = [category.lower() for category in ordered_categories]

    for file in file_names:

        # load synthetic responses from each file. 
        with open(file, "r") as file:
            synthetic_responses_by_group = json.load(file)

        # print(synthetic_responses_by_group)

        # if the response if a list of dictionaries then sum the responses
        if isinstance(synthetic_responses_by_group, list):

            aggregated_synthetic_responses = {}

            for entry in synthetic_responses_by_group:

                for response, count in entry["Synthetic Responses"].items():

                    # print("Response: ", response)
                    # print("Count: ", count)

                    if response in aggregated_synthetic_responses:
                        aggregated_synthetic_responses[response] += count
                    else:
                        print("Response: ", response)
                        print("Count: ", count)
                        aggregated_synthetic_responses[response] = count

            # implement a code to iterate through the ordered categories to check if they are in the synthetic responses
            for category in ordered_categories:

                if category not in aggregated_synthetic_responses:
                    aggregated_synthetic_responses[category] = 0

            # sort the synthetic responses in the order of the ordered categories
            aggregated_synthetic_responses = {key: aggregated_synthetic_responses[key] for key in ordered_categories}

            print(aggregated_synthetic_responses) 

            synthetic_responses.append(aggregated_synthetic_responses)

        else:

            synthetic_responses.append(synthetic_responses_by_group)

    x = range(len(synthetic_responses[0]))  # label locations

    fig, ax = plt.subplots()

    width = 0.15 # width of the bars

    for i in range(len(synthetic_responses)):
        rects = ax.bar([p + i * width for p in x], synthetic_responses[i].values(), width, label=f'Group {i+1}')

    ax.set_ylabel('Frequency') # set the y-axis label

    if question == "Demo":
        ax.set_title(f'Responses to Demo Question by Group')
    else:
        ax.set_title(f'Responses to Question {question} by Group')

    ax.set_xticks([p + width for p in x]) # set the x-axis ticks

    # format the ordered_categories to be in title case
    ordered_categories = ['\n'.join(wrap(l, 12)) for l in ordered_categories]

    ax.set_xticklabels(ordered_categories, rotation=90, fontsize=8) # set the x-axis labels

    plt.tight_layout() # adjust the layout of the plot

    age_groups = ["18-34", "35-54", "55 or older"]

    plt.legend(title="Age Group", labels=age_groups) # display the legend

    plt.savefig(f"C:\\Users\\haoch\\Documents\\COMP0190\\Data\\COMP0191-MSc-Project-Code\\Figures\\UKHLS-Hypothesis-2\\Question {question} by Group.png", bbox_inches='tight') # save the figure as a png

    plt.show() # display the plot

def test_visualise_responses_by_group():
    base_json_filepath = "C:\\Users\\haoch\\Documents\\COMP0190\\Data\\COMP0191-MSc-Project-Code\\Synthetic-Responses-JSON\\Hypothesis-2"

    demo_question_file_paths = []

    age_groups = ["18-34", "35-54", "55 or older"]

    for group in age_groups:
        demo_question_file_paths.append(base_json_filepath + f"\\question_1_{group}.json")

    visualise_responses_by_group(demo_question_file_paths, "Q1")

# test_visualise_responses_by_group()