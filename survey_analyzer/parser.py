import pandas as pd
import os

def load_dataset(file_path="data/nepal_earthquake.csv"):
    """
    Load the Nepal Earthquake dataset and return a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        print(f"CSV not found at: {file_path}")
        return None

    df = pd.read_csv(file_path)
    print(f"Dataset loaded successfully. Columns: {list(df.columns)}")
    return df