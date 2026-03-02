import pandas as pd

def analyze_numeric_column(col):
    """Analyze numeric column"""
    return {
        "count": col.count(),
        "mean": round(col.mean(), 2),
        "median": round(col.median(), 2),
        "std": round(col.std(), 2),
        "min": col.min(),
        "max": col.max()
    }

def analyze_categorical_column(col):
    """Analyze categorical column"""
    counts = col.value_counts(dropna=True)
    percentages = round((counts / col.count()) * 100, 2)
    summary = pd.DataFrame({"Count": counts, "Percentage": percentages})
    return summary

def analyze_column(df, column_name):
    
    if column_name not in df.columns:
        return {
            "error": f"Column '{column_name}' does not exist."
        }

    col = df[column_name]

    # Convert numeric-like values safely
    col_numeric = pd.to_numeric(col, errors='coerce')

    # If column behaves like numeric
    if col_numeric.notna().sum() > 0:

        return {
            "type": "numeric",
            "column": column_name,
            "count": int(col_numeric.count()),
            "mean": float(col_numeric.mean()),
            "median": float(col_numeric.median()),
            "min": float(col_numeric.min()),
            "max": float(col_numeric.max()),
            "std": float(col_numeric.std())
        }

    # Otherwise treat as categorical
    else:
        value_counts = col.value_counts()

        return {
            "type": "categorical",
            "column": column_name,
            "unique_values": int(col.nunique()),
            "top_values": value_counts.head(5).to_dict()
        }