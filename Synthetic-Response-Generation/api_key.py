# gets API key from "C:\Users\haoch\Documents\COMP0190\Data\API\key.txt"
def get_api_key():
    """
    Description: A function to get the OpenAI API key from a text file.

    Returns:
    •	The OpenAI API key.
    """
    path = "C:/Users/haoch/Documents/COMP0190/Data/API/key.txt" # set the path to the API key file
    with open(path, "r") as file:
        api_key = file.read().strip()

    return api_key

api_key = get_api_key()