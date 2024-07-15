import json

def load_environmental_distribution(name, wave_number):
    """
    Load the environmental distribution with the given name.

    Args:
        name (str): The name of the environmental distribution to load.
        wave_number (int): The wave number of the environmental distribution to load.

    Returns:
        dict: The environmental distribution.
    """

    if name == "scenv_crlf":
        file_path = f'C:\\Users\\haoch\\Documents\\COMP0190\\Data\\COMP0191-MSc-Project-Code\\Environmental-Views-Variables\\scenv_crlf\\Environmental Friendly Behaviour Probability Distribution Wave {wave_number}.json'

        with open(file_path, 'r') as f:
            return json.load(f)