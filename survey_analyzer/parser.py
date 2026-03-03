import pandas as pd
import os

def load_dataset(file_path=None):
    """
    Load the Nepal Earthquake dataset and return a pandas DataFrame.
    
    Parameters:
    - file_path (str): Absolute or relative path to CSV. If None, defaults to
      'data/nepal_earthquake.csv' relative to project root.
    
    Returns:
    - df (pandas.DataFrame) or None if file not found
    """
    if file_path is None:
        # Default relative path
        file_path = os.path.join("data", "nepal_earthquake.csv")

    # Convert to absolute path
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        print(f"CSV not found at: {file_path}")
        return None

    df = pd.read_csv(file_path)
    print(f"Dataset loaded successfully. Columns: {list(df.columns)}")
    
    # Optional: remove fully empty columns
    df.dropna(axis=1, how="all", inplace=True)
    
    return df