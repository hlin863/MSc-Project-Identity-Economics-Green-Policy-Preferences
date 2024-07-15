import random
 
def generate_age_group_prompt(age_group_probability_dict):
    """
    Generate a prompt for the synthetic individual's age group.

    Parameters:
    age_group_probability_dict (dict): A dictionary containing the age group probabilities.

    Returns:
    str: A prompt indicating the synthetic individual's age group.
    """
    # write a prompt to generate the profile of the synthetic individual's age group
    age_group = random.choices(list(age_group_probability_dict.keys()), list(age_group_probability_dict.values()))[0]

    age_group_prompt = f"In terms of my age, my age group is {age_group}."

    return age_group_prompt

def generate_highest_qualification_prompt(education_levels_probability_dict):
    """
    Generate a prompt for the synthetic individual's highest qualification.

    Parameters:
    education_levels_probability_dict (dict): A dictionary containing education levels as keys and their corresponding probabilities as values.

    Returns:
    str: A prompt describing the synthetic individual's highest qualification.
    """

    highest_qualification = random.choices(list(education_levels_probability_dict.keys()), list(education_levels_probability_dict.values()))[0]

    highest_qualification_prompt = "In terms of my qualifications, "

    if highest_qualification == "None":
        highest_qualification_prompt += "I do not have any qualifications."
    else: 
        highest_qualification_prompt += f"My highest qualification is {highest_qualification}."

    return highest_qualification_prompt

def generate_ethnic_group_prompt(ethnicity_probability_distribution_dict):
    """
    Generate a prompt for the profile of a synthetic individual based on the given ethnicity probability distribution.

    Parameters:
    ethnicity_probability_distribution_dict (dict): A dictionary representing the probability distribution of ethnicities.

    Returns:
    str: A prompt indicating the racial identity of the synthetic individual.
    """
    ethnic_group = random.choices(list(ethnicity_probability_distribution_dict.keys()), list(ethnicity_probability_distribution_dict.values()))[0]

    ethnic_group_prompt = f"Racially, I am {ethnic_group}."

    return ethnic_group_prompt

def generate_current_job_prompt(current_job_probability_distribution_dict):
    """
    Generate a prompt for the profile of a synthetic individual based on their current job.

    Parameters:
    current_job_probability_distribution_dict (dict): A dictionary containing the probability distribution of current jobs.

    Returns:
    str: A prompt describing the profession of the synthetic individual.
    """
    current_job = random.choices(list(current_job_probability_distribution_dict.keys()), list(current_job_probability_distribution_dict.values()))[0]

    current_job_prompt = f"My profession is {current_job}."

    return current_job_prompt

def generate_income_prompt(current_job_prompt):
    """
    Generates a random income value based on the given current job prompt.

    Args:
        current_job_prompt (str): The current job prompt.

    Returns:
        float: A random income value within the range specified for the given current job prompt.
    """
    # remove ""My profession is " from the current_job_prompt
    role = current_job_prompt.replace("My profession is ", "")

    # remove full stop from the current_job_prompt
    role = role.replace(".", "")

    # print statement to check the role variable
    # print(role)
   
    if role == 'Higher Managerial and Administrative':
        random_income = random.randint(10000, 12500)
    elif role == 'Large Establishments':
        random_income = random.randint(9167, 11667)
    elif role == 'Higher Professional':
        random_income = random.randint(8333, 10833)
    elif role == 'Lower Managerial and Supervisory':
        random_income = random.randint(6667, 9167)
    elif role == 'Lower Professional and Technical':
        random_income = random.randint(5833, 8333)
    elif role == 'Intermediate Occupations':
        random_income = random.randint(5000, 7500)
    elif role == 'Lower Supervisory and Technical':
        random_income = random.randint(4167, 6667)
    elif role == 'Small Establishments and Own Account Workers':
        random_income = random.randint(3333, 5833)
    elif role == 'Semi-Routine Occupations':
        random_income = random.randint(2917, 5417)
    elif role == 'Routine Occupations':
        random_income = random.randint(2500, 5000)
    else:
        # raise an exception if the role is not found
        raise ValueError("The role is not found.")

    random_income = round(random_income, 2)

    income_prompt = f"Financially, my monthly income is £{random_income}."

    return income_prompt

def generate_gender_prompt(gender_probability_distribution_dict):
    """
    Generate a prompt for the profile of a synthetic individual based on a given gender probability distribution.

    Parameters:
    gender_probability_distribution_dict (dict): A dictionary representing the probability distribution of genders.

    Returns:
    str: A prompt string indicating the generated gender.

    Example:
    >>> gender_probability_distribution_dict = {'Male': 0.4, 'Female': 0.6}
    >>> generate_gender_prompt(gender_probability_distribution_dict)
    'I am Female.'
    """

    gender = random.choices(list(gender_probability_distribution_dict.keys()), list(gender_probability_distribution_dict.values()))[0]

    gender_prompt = f"I am {gender}."

    return gender_prompt

def generate_marital_status_prompt(martial_probability_distribution_dict):
    """
    Generate a prompt for the marital status based on a given probability distribution.

    Parameters:
    martial_probability_distribution_dict (dict): A dictionary representing the probability distribution of marital statuses.

    Returns:
    str: A string representing the generated marital status prompt.
    """

    marital_status = random.choices(list(martial_probability_distribution_dict.keys()), list(martial_probability_distribution_dict.values()))[0]

    marital_status_prompt = f"My marital status is {marital_status}."

    return marital_status_prompt

def generate_residence_prompt(residence_probability_distribution_dict):
    """
    Generate a residence prompt based on a given residence probability distribution.

    Parameters:
    residence_probability_distribution_dict (dict): A dictionary representing the probability distribution of different residence types.

    Returns:
    str: A residence prompt based on the randomly selected residence type.
    """

    residence = random.choices(list(residence_probability_distribution_dict.keys()), list(residence_probability_distribution_dict.values()))[0]

    if residence == "Urban":
        residence_prompt = "I live in an urban area." # if the residence is urban
    elif residence == "Rural":
        residence_prompt = "I live in a rural area." # if the residence is rural
    else:
        residence_prompt = f"I live in a {residence} area."

    return residence_prompt

def generate_region_prompt(region_probability_distribution_dict):
    """
    Generate a region prompt based on a given region probability distribution.

    Parameters:
    region_probability_distribution_dict (dict): A dictionary representing the probability distribution of different regions.

    Returns:
    str: A region prompt based on the randomly selected region.
    """

    region = random.choices(list(region_probability_distribution_dict.keys()), list(region_probability_distribution_dict.values()))[0]

    region_prompt = f"I live in the {region} region."

    return region_prompt

def generate_number_of_children_prompt(number_of_children_probability_distribution_dict):
    """
    Generate a prompt based on the number of children.

    Parameters:
    - number_of_children_probability_distribution_dict (dict): A dictionary representing the probability distribution of the number of children.

    Returns:
    - number_of_children_prompt (str): A string representing the generated prompt based on the number of children.
    """

    number_of_children = random.choices(list(number_of_children_probability_distribution_dict.keys()), list(number_of_children_probability_distribution_dict.values()))[0]

    if number_of_children == "1":
        number_of_children_prompt = "I have 1 child."
    elif number_of_children == "0":
        number_of_children_prompt = "I do not have any children."
    else:
        number_of_children_prompt = f"I have {number_of_children} children."

    return number_of_children_prompt

def generate_voting_intention_prompt(voting_intention_probability_distribution_dict):
    """
    Generates a voting intention prompt based on a given probability distribution.

    Parameters:
    voting_intention_probability_distribution_dict (dict): A dictionary representing the probability distribution of voting intentions.

    Returns:
    str: A string representing the generated voting intention prompt.
    """

    voting_intention = random.choices(list(voting_intention_probability_distribution_dict.keys()), list(voting_intention_probability_distribution_dict.values()))[0]

    # check if the voting intention contains the word "Party"
    if "Party" in voting_intention:
        voting_intention_prompt = f"Ideologically, I describe myself as a {voting_intention} supporter."
    else:
        voting_intention_prompt = f"Ideologically, I describe myself as a {voting_intention} Party supporter."

    return voting_intention_prompt