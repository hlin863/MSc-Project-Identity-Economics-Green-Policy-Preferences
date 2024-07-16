from profile_conditioning import generate_current_job_prompt, generate_residence_prompt, generate_region_prompt, generate_number_of_children_prompt, generate_voting_intention_prompt, generate_income_prompt, generate_age_group_prompt, generate_highest_qualification_prompt
from load_probability_distributions import *
import random

def generate_gender_substring(gender):

    return f"I am {gender}."

def generate_marital_status_substring(marital_status):

    return f"My marital status is {marital_status}."

def generate_qualification_substring(highest_qualification):

    highest_qualification_prompt = "In terms of my qualifications, "

    if highest_qualification == "None":
        highest_qualification_prompt += "I do not have any qualifications."
    else: 
        highest_qualification_prompt += f"My highest qualification is {highest_qualification}."

    return highest_qualification_prompt

def generate_ethnicity_substring(ethnic_group):
    ethnic_group_prompt = f"Racially, I am {ethnic_group}."

    return ethnic_group_prompt

def generate_number_of_children_substring(number_of_children):

    if number_of_children == "1":
        number_of_children_prompt = "I have 1 child."
    elif number_of_children == "0":
        number_of_children_prompt = "I do not have any children."
    else:
        number_of_children_prompt = f"I have {number_of_children} children."

    return number_of_children_prompt

def generate_region_substring(region):

    region_prompt = f"I live in the {region}."

    return region_prompt

def generate_urban_rural_substring(urban_rural):

    if urban_rural == "Urban":
        urban_rural_prompt = "I live in an urban area."
    else:
        urban_rural_prompt = "I live in a rural area."

    return urban_rural_prompt

def generate_agegroup_substring(age_group):

    age_group_prompt = f"In terms of my age, my age group is {age_group}."

    return age_group_prompt

def generate_job_substring(current_job):

    # data path of the probability distributions: C:\Users\haoch\Documents\COMP0190\Data\COMP0191-MSc-Project-Code\UKHLS-Profiling-Data
    data_path = "C:/Users/haoch/Documents/COMP0190/Data/COMP0191-MSc-Project-Code/UKHLS-Profiling-Data"

    current_job_probability_distribution_dicts = load_probability_distributions(data_path + "/Current Job")

    return generate_current_job_prompt(current_job_probability_distribution_dicts[len(current_job_probability_distribution_dicts) - 1])

def generate_voting_intention_substring(voting_intention):

    if "Party" in voting_intention:
        voting_intention_prompt = f"Ideologically, I describe myself as a {voting_intention} supporter."
    else:
        voting_intention_prompt = f"Ideologically, I describe myself as a {voting_intention} Party supporter."

    return voting_intention_prompt

def generating_income_substring(role):

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
        random_income = random.randint(2500, 5000)

    random_income = round(random_income, 2)

    income_prompt = f"Financially, my monthly income is £{random_income}."

    return income_prompt

def visualise_profile_and_opinion_string(profile, response_variable, opinion):

    gender_substring = generate_gender_substring(profile["sex"])

    marital_status_substring = generate_marital_status_substring(profile["marstat"])

    qualification_substring = generate_qualification_substring(profile["qfhigh"])

    ethnicity_substring = generate_ethnicity_substring(profile["racel_dv"])

    number_of_children_substring = generate_number_of_children_substring(profile["lnprnt"])

    region_substring = generate_region_substring(profile["gor_dv"])

    urban_rural_substring = generate_urban_rural_substring(profile["urban_dv"])

    agegroup_substring = generate_agegroup_substring(profile["agegr10_dv"])

    job_substring = generate_job_substring(profile["jbnssec_dv"])

    voting_intention_substring = generate_voting_intention_substring(profile["vote3"])

    income_substring = generating_income_substring(profile["jbnssec_dv"])

    opinion_substring = opinion

    # concatenate the substrings to form the profile and opinion string
    profile_string = f"{gender_substring} {marital_status_substring} {qualification_substring} {ethnicity_substring} {number_of_children_substring} {region_substring} {urban_rural_substring} {agegroup_substring} {job_substring} {voting_intention_substring} {income_substring}" 

    if response_variable == "scenv_crlf":

        profile_string += "When I asked to write my response to the question, \"And which of these would you say best describes your current lifestyle?\", I respond with: "

    return profile_string, opinion_substring

def visualise_ukhls_profile_and_response(data, response_variable):
    # first initialise profile as data columns except the variable "scenv_crlf"
    profile = data.drop(columns=[response_variable])

    # initialise the response as the variable "scenv_crlf"
    opinion = data[response_variable]

    profile_string, opinion_string = visualise_profile_and_opinion_string(profile, response_variable, opinion)

    return profile_string, opinion_string