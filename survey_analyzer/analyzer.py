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
    """Analyze a column based on its type"""
    if column_name not in df.columns:
        return f"Column '{column_name}' does not exist!"
    
    col = df[column_name]

    # Convert numeric-ish strings to floats if possible
    if col.dtype == 'object':
        col = pd.to_numeric(col, errors='coerce')  # converts to float, NaN if fails
    
    if pd.api.types.is_numeric_dtype(col):
        result = analyze_numeric_column(col)
        summary = "\n".join([f"{k}: {v}" for k, v in result.items()])
        return f"Numeric Analysis for '{column_name}':\n{summary}"
    else:
        summary_df = analyze_categorical_column(col)
        return f"Categorical Analysis for '{column_name}':\n{summary_df.to_string()}"