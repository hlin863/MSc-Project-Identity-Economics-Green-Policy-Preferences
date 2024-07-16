from generate_subprompts import * # import all the subprompts to help shaping synthetic user profiles. 
from load_probability_distributions import * # import the probability distributions to help shaping synthetic user profiles.

def load_all_probability_distributions():

    # data path of the probability distributions: C:\Users\haoch\Documents\COMP0190\Data\COMP0191-MSc-Project-Code\UKHLS-Profiling-Data
    data_path = "C:/Users/haoch/Documents/COMP0190/Data/COMP0191-MSc-Project-Code/UKHLS-Profiling-Data"

    # age group probability distributions
    age_group_probability_dicts = load_probability_distributions(data_path + "/Age Groups")

    # highest qualification distributions
    highest_qualification_probability_dicts = load_probability_distributions(data_path + "/Highest Qualifications")

    # ethnic group distributions
    ethnic_group_probability_dicts = load_probability_distributions(data_path + "/Ethnicity")

    # current job distributions
    current_job_probability_dicts = load_probability_distributions(data_path + "/Current Job")

    # gender distributions
    gender_probability_dicts = load_probability_distributions(data_path + "/Gender")

    # marital status distributions
    marital_status_probability_dicts = load_probability_distributions(data_path + "/Marital Status")

    # number of children distributions
    number_of_children_probability_dicts = load_probability_distributions(data_path + "/Number of Children")

    # residence distributions
    residence_probability_dicts = load_probability_distributions(data_path + "/Residence")

    # region distributions
    region_probability_dicts = load_probability_distributions(data_path + "/Region")

    # voting intention distributions
    voting_intention_probability_dicts = load_probability_distributions(data_path + "/Voting Intentions")

    return age_group_probability_dicts, highest_qualification_probability_dicts, ethnic_group_probability_dicts, current_job_probability_dicts, gender_probability_dicts, marital_status_probability_dicts, residence_probability_dicts, region_probability_dicts, number_of_children_probability_dicts, voting_intention_probability_dicts

def generate_profiling_subprompts(wave_number, by_group, *args):
    """
    Description: A function to generate the subprompts for the synthetic individual's profile.
    The function is dynamically adjustable to the wave number of the UKHLS study to help identifying how views on the environment have changed over time.

    Parameters:
    •	wave_number (int): The wave number of the UKHLS study.
    • by_group (int): an integer value to determine if the function is simulating synthetic responses by group and which group is the function is testing for. (default is 0)
    • args (list): a list of arguments to help the function generate the subprompts for the synthetic individual's profile by group.

    Returns:
    •	A list of subprompts for the synthetic individual's profile.
    """
    age_group_probability_dicts, education_probability_dicts, ethnicity_probability_dicts, current_job_probability_dicts, gender_probability_dicts, marital_status_probability_dicts, residence_probability_dicts, region_probability_dicts, number_of_children_probability_dicts, voting_intention_probability_dicts = load_all_probability_distributions()

    if args:
        group = args[0]

    if by_group == 1:
        # simulating responses to environmental issues by age group to see how views on environmental issues differ by age.
        age_group_prompt = f"In terms of my age, my age group is {group}"
    else: 
        # generate the profile of the synthetic individual's age group
        age_group_prompt = generate_age_group_prompt(age_group_probability_dicts[wave_number - 1])

    if by_group == 2:
        highest_qualification_prompt = f"In terms of my qualifications. My highest qualification is {group}"
    else:
        # generate the profile of the synthetic individual's highest qualification
        highest_qualification_prompt = generate_highest_qualification_prompt(education_probability_dicts[wave_number - 1]) 

    if by_group == 3:
        ethnic_group_prompt = f"Racially, I am {group}."
    else:
        # generate the profile of the synthetic ethnic groups. 
        ethnic_group_prompt = generate_ethnic_group_prompt(ethnicity_probability_dicts[wave_number - 1])

    if by_group == 4:
        current_job_prompt = f"My profession is {group}."
    else:
        # generate the profile of the synthetic individual's current job
        current_job_prompt = generate_current_job_prompt(current_job_probability_dicts[wave_number - 1])

    if by_group == 5:
        income_prompt = f"Financially, my monthly income is {group}."
    else:
        # generate the profile of the synthetic individual's gross monthly income
        income_prompt = generate_income_prompt(current_job_prompt)

    if by_group == 6:
        gender_prompt = f"I am {group}."
    else:
        if wave_number == 13:
            # generate the profile of the synthetic gender group.
            gender_prompt = generate_gender_prompt(gender_probability_dicts[11])
        else:
            gender_prompt = generate_gender_prompt(gender_probability_dicts[wave_number - 1])

    if by_group == 7:
        marital_status_prompt = f"My marital status is {group}."
    else:
        if wave_number == 13:
            # generate the profile of the synthetic marital status group.
            marital_status_prompt = generate_marital_status_prompt(marital_status_probability_dicts[11])
        else:
            # generate the profile of the synthetic marital status group.
            marital_status_prompt = generate_marital_status_prompt(marital_status_probability_dicts[wave_number - 1])

    if by_group == 8:
        if group == "urban":
            residence_prompt = f"I live in an urban area."
        elif group == "rural":
            residence_prompt = f"I live in a rural area."
    else:
        if wave_number == 13:
            # generate the profile of the synthetic residence group.
            residence_prompt = generate_residence_prompt(residence_probability_dicts[11])
        else:
            # generate the profile of the synthetic residence group.
            residence_prompt = generate_residence_prompt(residence_probability_dicts[wave_number - 1])

    if by_group == 9:
        region_prompt = f"I live in the {group} region."
    else:
        if wave_number == 13:
            region_prompt = generate_region_prompt(region_probability_dicts[11])
        else:
            region_prompt = generate_region_prompt(region_probability_dicts[wave_number - 1])

    if by_group == 10:
        if group == "0":
            number_of_children_prompt = f"I have no children."
        elif group == "1":
            number_of_children_prompt = f"I have one child."
        else:
            number_of_children_prompt = f"I have {group} children."
    else:
        if wave_number == 13:
            # generate the profile of the synthetic number of children group.
            number_of_children_prompt = generate_number_of_children_prompt(number_of_children_probability_dicts[11])
        else:
            # generate the profile of the synthetic number of children group.
            number_of_children_prompt = generate_number_of_children_prompt(number_of_children_probability_dicts[wave_number - 1])

    if by_group == 11:

        if party in group:
            voting_intention_prompt = f"Ideologically, I describe myself as a {group} supporter."
        else:
            voting_intention_prompt = f"Ideologically, I describe myself as a {group} Party supporter."

    else:
        voting_distribution_indexes = [1, 2, 3, 4, 5, 6, 7, 9, 10]

        if wave_number in voting_distribution_indexes:
            # generate the subprompt for the synthetic individual's voting intention
            voting_intention_prompt = generate_voting_intention_prompt(voting_intention_probability_dicts[wave_number - 1])
        else:
            # generate the subprompt for the synthetic individual's voting intention
            voting_intention_prompt = generate_voting_intention_prompt(voting_intention_probability_dicts[9])

    return income_prompt, age_group_prompt, highest_qualification_prompt, ethnic_group_prompt, current_job_prompt, gender_prompt, marital_status_prompt, residence_prompt, region_prompt, number_of_children_prompt, voting_intention_prompt

# tests profile conditioning
for i in range(1, 14): # test the function for 13 waves of UKHLS data. 
    print(generate_profiling_subprompts(i, 1, "18 - 34")) 
    # run a test to generate the subprompts for the synthetic individual's profile for the first wave of the UKHLS study