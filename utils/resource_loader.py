import pandas as pd
    
def load_list(file_name: str):
    return pd.read_csv(file_name, header=None, keep_default_na=False)[0].to_list()