import os
import json

def load_probability_distributions(path):

    file_names = os.listdir(path)

    # load all the json files containing the age group probability distributions
    probability_dicts = []

    for file_name in file_names:

        with open(f"{path}/{file_name}", "r") as file:
            probability_dict = json.load(file)

            probability_dicts.append(probability_dict)

    return probability_dicts

# tests load_age_group_probability_distributions
def test_load_age_group_probability_distributions():
    path = "C:/Users/haoch/Documents/COMP0190/Data/COMP0191-MSc-Project-Code/UKHLS-Profiling-Data/Age Groups"
    age_group_probability_dicts = load_probability_distributions(path)

    assert len(age_group_probability_dicts) == 13
    assert all(isinstance(age_group_probability_dict, dict) for age_group_probability_dict in age_group_probability_dicts)

    print("load_age_group_probability_distributions PASSED")

def test_load_highest_qualification_distributions():
    path = "C:/Users/haoch/Documents/COMP0190/Data/COMP0191-MSc-Project-Code/UKHLS-Profiling-Data/Highest Qualifications"
    highest_qualification_probability_dicts = load_probability_distributions(path)

    assert len(highest_qualification_probability_dicts) == 13
    assert all(isinstance(highest_qualification_probability_dict, dict) for highest_qualification_probability_dict in highest_qualification_probability_dicts)

    print("load_highest_qualification_distributions PASSED")

test_load_highest_qualification_distributions()