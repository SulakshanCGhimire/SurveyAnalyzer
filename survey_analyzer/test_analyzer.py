from parser import load_csv
from analyzer import analyze_column

df = load_csv()

# Test numeric column
print(analyze_column(df, "Hazard (Intensity)"))

# Test categorical column
print(analyze_column(df, "DISTRICT"))

# Optional: list all numeric and categorical columns automatically
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
print("Numeric columns:", numeric_cols)
print("Categorical columns:", categorical_cols)