import numpy as np
import pandas as pd
from load_stata import load_stata_file

# lists to map the different education levels to standardise comparison between different education levels. 
no_formal_education_list = ["None of the above"]

secondary_education_list = [
    "GCSE / O Level", "A Level", "AS Level", "Credit Standard Grade / Ordinary (O) Grade (National 5 / Intermediate 2)",
    "CSE", "Other school (inc. school leaving exam certificate or matriculation)", "Higher Grade",
    "General Standard Grade (National 4 / Intermediate 1)", "Foundation Standard Grade (National 3 / Access 3)",
    "Advanced Higher / Scottish Baccalaureate", "Advanced Higher", "International Baccalaureate",
    "Certificate of sixth year studies"
]

post_secondary_education_list = [
    "Diploma in higher education", "Foundation degree", "Access to Higher Education (HE) Diploma",
    "Teaching qualification (excluding PGCE)", "Teach qual prim (excl PGCE)", "Teach qual sec/further ed (excel PGCE)"
]

higher_education_list = [
    "University Higher Degree (e.g. MSc, PhD)", "First degree level qualification including foundation degrees, graduate membership of a professional Institute, PGCE",
    "First degree level qualification (e.g., BA, BSc)", "PGCE or equivalent", "Nursing or other medical qualification not yet mentioned"
]

def removing_irrelevant_columns(data):

    data = data.drop(columns=["pidp", "hidp", "fihhmnlabgrs_dv"])

    return data

def removing_nan_columns(data):

    nan_columns = data.columns[data.isnull().any()].tolist() # get a list of column names in data with nan values.

    data_cleaned = data.dropna(subset=nan_columns) # remove nan values from the data

    return data_cleaned

def count_invalid_values(special_values, column_data):
    count = 0
    
    for value in column_data:
        # if the value is a string and it is in the special values list
        if isinstance(value, str) and value.lower() in special_values:
            count += 1
        elif value in special_values:
            count += 1

def get_preprocessed_distribution(distribution):

    # remove responses containing "inapplicable" from the data distribution
    distribution = distribution[distribution != "inapplicable"]

    # recalculate the probability distribution of the distribution
    probability_distribution = distribution.value_counts(normalize=True).to_dict()

    # remove probabilities with values of 0
    probability_distribution = {key: value for key, value in probability_distribution.items() if value != 0}

    return probability_distribution

def impute_missing_responses(distribution, prob_distribution):
    # Identify the indices of the "missing", "don't know", and "refusal" responses
    indices_to_impute = distribution[(distribution == "inapplicable")].index

    # List of values and their corresponding probabilities
    values = list(prob_distribution.keys())
    probabilities = list(prob_distribution.values())

    # Randomly assign values based on the probability distribution
    imputed_values = np.random.choice(values, size=len(indices_to_impute), p=probabilities)

    # Ensure that all imputed values are valid categories in the distribution
    all_categories = set(distribution.cat.categories).union(values)
    
    distribution = distribution.cat.set_categories(all_categories)

    for i, index in enumerate(indices_to_impute):
        try:
            distribution.loc[index] = imputed_values[i]
        except Exception as e:
            pass

    return distribution

def remove_invalid_responses(data, column):

    column_data = data[column] # get the column data

    special_values = ["invalid", "refusal", "don't know", "missing"]
    
    count_invalid_values(special_values, column_data)

    # remove the entries with invalid responses
    data = data[~column_data.isin(special_values)]

    column_data = data[column] # get the column data
    
    count_invalid_values(special_values, column_data)

    return data

def numerical_mapping(data, column):

    if column == "qfhigh":

        data[column] = data[column].replace(19.0, "PGCE or equivalent")

        data[column] = data[column].replace(20.0, "First degree level qualification (e.g., BA, BSc)")

        data[column] = data[column].replace(21.0, "Foundation degree")

        data[column] = data[column].replace(22.0, "Teach qual sec/further ed (excel PGCE)")

        data[column] = data[column].replace(23.0, "Teach qual prim (excl PGCE)")

        data[column] = data[column].replace(24.0, "Access to Higher Education (HE) Diploma")

        data[column] = data[column].replace(25.0, "Advanced Higher")

    if column == "vote3":

        data[column] = data[column].replace(14, "Brexit Party")

        data[column] = data[column].replace(15, "Change UK Party")

    return data

# Define mapping function
def map_qualification(response):
    if response in no_formal_education_list:
        return "No formal education"
    elif response in secondary_education_list:
        return "Secondary education"
    elif response in post_secondary_education_list:
        return "Post-secondary education"
    elif response in higher_education_list:
        return "Higher education"
    else:
        return response

def simplify_qualification(data_column):

    data_column = data_column.apply(map_qualification)

    return data_column
    
def simplify_voting_intention(data_column):

    # print(data_column.unique())

    # initialise a list storing a list of other parties as a list data_column.unique after removing "Conservatives", "Labour", "Scottish National Party" and "Liberal Democrats"
    other_party_list = [party for party in data_column.unique() if party not in ["Conservatives", "Labour", "Liberal Democrat"]]

    # replace the other parties with "Other"
    data_column = data_column.replace(other_party_list, "Other")

    return data_column

def simplify_marital_status(data_column):
    
    marital_status_map = {
        "Single, nvr marr/civ p": "Single",
        "Separated legally marr": "Separated",
        "Sep from Civil Partner ": "Separated",
        "Civil Partner (legal)": "Civil Partner"
    }

    # apply the mapping to the marital status column
    data_column = data_column.replace(marital_status_map)

    return data_column

def ethnicity_simplification(data_column):
    
    data_column = data_column.replace("british/english/scottish/welsh/northern irish (white)", "British")

    data_column = data_column.replace("indian (asian or asian british)", "Indian")

    data_column = data_column.replace("pakistani (asian or asian british)", "Pakistani")

    data_column = data_column.replace("any other white background (white)", "Other Ethnicities")

    data_column = data_column.replace("bangladeshi (asian or asian british)", "Bangladeshi")

    data_column = data_column.replace("chinese (asian or asian british)", "Chinese")

    data_column = data_column.replace("irish (white)", "Irish")

    data_column = data_column.replace("african (black or black britih)", "African")

    data_column = data_column.replace("caribbean (black or black british)", "Caribbean")

    data_column = data_column.replace("any other asian background (asian or asian british)", "Other Ethnicities")

    data_column = data_column.replace("any other black background (black or black britih)", "Other Ethnicities")

    data_column = data_column.replace("white and asian (mixed)", "Mixed")

    data_column = data_column.replace("white and black african (mixed)", "Mixed")

    data_column = data_column.replace("white and black caribbean (mixed)", "Mixed")

    data_column = data_column.replace("arab (other ethnic group)", "Arab")

    data_column = data_column.replace("any other ethnic group (other ethnic group)", "Mixed")

    data_column = data_column.replace("any other mixed background (mixed)", "Mixed")

    return data_column

def category_simplification(data, column):

    if column == "qfhigh":

        data[column] = simplify_qualification(data[column])

    if column == "vote3":

        data[column] = simplify_voting_intention(data[column])

    if column == "marstat":

        data[column] = simplify_marital_status(data[column])

    if column == "racel_dv":

        data[column] = ethnicity_simplification(data[column])

    return data

def preprocess_stata_data(data):

    data = removing_irrelevant_columns(data) # removing irrelevant columns from the data. 

    data = removing_nan_columns(data) # remove nan values from the data

    # get a list of column names for the data
    columns = data.columns

    for column in columns:
        data = remove_invalid_responses(data, column)

        if column == "scenv_crlf":
            # remove responses containing proxy and inapplicable from the data
            data = data[~data[column].isin(["proxy", "inapplicable"])]

    qualification_probability_distribution = get_preprocessed_distribution(data["qfhigh"])

    data["qfhigh"] = impute_missing_responses(data["qfhigh"], qualification_probability_distribution)

    number_of_children_distribution = get_preprocessed_distribution(data["lnprnt"])

    data["lnprnt"] = impute_missing_responses(data["lnprnt"], number_of_children_distribution)

    for column in columns:
        data = numerical_mapping(data, column)

        data = category_simplification(data, column)

    return data

# Example usage:
# Assuming `stata_demo_question_responses_wave_ten` is the DataFrame to be preprocessed
def test_preprocess_stata_data_function():
    stata_demo_question_filepath = "C:\\Users\\haoch\\Documents\\COMP0190\\Data\\COMP0191-MSc-Project-Code\\Stata-Results\\UKHLS_demo_responses.dta"

    stata_demo_question_responses = load_stata_file(stata_demo_question_filepath)

    stata_demo_question_responses_wave_eight, stata_demo_question_responses_wave_nine, stata_demo_question_responses_wave_ten = [stata_demo_question_responses[stata_demo_question_responses["wavename"] == wavename] for wavename in [8.0, 9.0, 10.0]]

    stata_demo_question_responses_wave_ten_preprocessed = preprocess_stata_data(stata_demo_question_responses_wave_ten)

    print(stata_demo_question_responses_wave_ten_preprocessed)