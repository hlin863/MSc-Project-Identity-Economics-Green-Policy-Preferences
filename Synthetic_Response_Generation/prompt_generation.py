from profile_conditioning import generate_profiling_subprompts

def get_response_option_prompt(question, potential_answers):
    """
    Generates a prompt with response options for the user.

    Parameters:
    potential_answers (list): A list of potential answers that the user can choose from.

    Returns:
    str: The base prompt before the response options are added. 
    str: A prompt with the response options.

    Example:
    >>> get_response_option_prompt(['Yes', 'No', 'Maybe'])
    'You can respond with one of the following options: Yes, No, Maybe'
    """
    response_options_base = f"Given your profile as a UKHLS survey respondent, answer this question or statement \"{question}\" using only one of the following options: "

    # initialise a subprompt to store the response options
    response_options = response_options_base

    # add the potential answers to the response options as a bullet point list
    for i, potential_answer in enumerate(potential_answers):
        response_options += f"\n{i+1}. {potential_answer}"

    return response_options_base, response_options

def test_response_option_prompt_function():
    """
    Test function for the get_response_option_prompt function.
    """
    test_question = "To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?"
    test_potential_answers = ["Strongly agree", "Tend to agree", "Neither agree nor disagree", "Tend to disagree", "Strongly disagree"]

    response_options_base, response_options = get_response_option_prompt(test_question, test_potential_answers)

    assert response_options_base == "Given your profile as a UKHLS survey respondent, answer this question or statement \"To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?\" using only one of the following options: "
    assert response_options == "Given your profile as a UKHLS survey respondent, answer this question or statement \"To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?\" using only one of the following options: \n1. Strongly agree\n2. Tend to agree\n3. Neither agree nor disagree\n4. Tend to disagree\n5. Strongly disagree"

    print("test_response_option_prompt_function PASSED")

def get_system_and_user_prompts(question, potential_answers, wave_number):

    system_prompts = []

    income_prompt, age_group_prompt, highest_qualification_prompt, ethnic_group_prompt, current_job_prompt, gender_prompt, marital_status_prompt, residence_prompt, region_prompt, number_of_children_prompt, voting_intention_prompt = generate_profiling_subprompts(wave_number)

    demographic_profiles = [income_prompt, age_group_prompt, highest_qualification_prompt, ethnic_group_prompt, current_job_prompt, gender_prompt, marital_status_prompt, residence_prompt, region_prompt, number_of_children_prompt, voting_intention_prompt]

    profiling_prompt = "You are a respondent to the UKHLS survey with the following profile \""

    for profile_subprompt in demographic_profiles:
        profiling_prompt += profile_subprompt + "\n"

    profiling_prompt += "\". "

    system_prompts.append(profiling_prompt)

    system_question_context_prompt = "Use your identities and socio-economic background to understand your preferences toward green policies by answering questions about attitudes to environmental policies. "

    system_prompts.append(system_question_context_prompt) # add the survey question prompt to the system prompts

    user_prompts = []

    responses_options_base, response_options = get_response_option_prompt(question, potential_answers)

    # add the response options to the system prompts
    user_prompts.append(response_options)

    return system_prompts, user_prompts

def test_get_system_and_user_prompts_function():
    """
    Test function for the get_system_and_user_prompts function.
    """
    test_question = "To what extent do you agree with the statement: I think of myself as an environmentally friendly consumer?"
    test_potential_answers = ["Strongly agree", "Tend to agree", "Neither agree nor disagree", "Tend to disagree", "Strongly disagree"]
    test_wave_number = 1

    system_prompts, user_prompts = get_system_and_user_prompts(test_question, test_potential_answers, test_wave_number)

    assert len(system_prompts) == 2
    assert len(user_prompts) == 1

    print("test_get_system_and_user_prompts_function PASSED")