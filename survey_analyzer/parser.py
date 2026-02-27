import pandas as pd

def load_csv(file_path="C:\\Users\\suluc\\Desktop\\SurveyAnalyzer\\data\\nepal_earthquake.csv"):
    """
    Load the Nepal Earthquake dataset and return a pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame or None: Loaded dataset or None if file not found
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully. Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print("CSV file not found! Make sure the CSV is in the 'data/' folder")
        return None

# Quick test
if __name__ == "__main__":
    df = load_csv()
    if df is not None:
        print(df.head())  # Show first 5 rows