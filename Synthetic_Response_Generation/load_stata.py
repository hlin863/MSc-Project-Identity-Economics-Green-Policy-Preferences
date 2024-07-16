import pandas as pd

def load_stata_file(file_path):
    stata_file = pd.read_stata(file_path)

    return stata_file