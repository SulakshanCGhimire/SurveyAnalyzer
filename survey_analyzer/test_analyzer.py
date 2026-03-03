from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column
from pprint import pprint

def test_column(df, column_name):
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in dataset.")
        return
    result = analyze_column(df, column_name)
    print(f"\nAnalysis Result for '{column_name}':")
    pprint(result)
    print("-" * 50)

if __name__ == "__main__":
    # Load dataset
    df = load_dataset("data/nepal_earthquake.csv")
    if df is None:
        print("Failed to load dataset.")
        exit(1)

    # Columns to test
    numeric_columns = ["Hazard (Intensity)", "Exposure", "Housing", "Poverty", "Vulnerability", "Severity", "Severity Normalized"]
    categorical_columns = ["P_CODE", "VDC_NAME", "DISTRICT", "REGION", "Severity category"]

    print("\n=== Numeric Columns Test ===")
    for col in numeric_columns:
        test_column(df, col)

    print("\n=== Categorical Columns Test ===")
    for col in categorical_columns:
        test_column(df, col)