from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column

# Load dataset
df = load_dataset("data/nepal_earthquake.csv")

# Test numeric column
result_numeric = analyze_column(df, "Hazard (Intensity)")
print("Numeric Test:")
print(result_numeric)

print("\n----------------------\n")

# Test categorical column
result_categorical = analyze_column(df, "DISTRICT")
print("Categorical Test:")
print(result_categorical)