import pandas as pd

def analyze_numeric_column(col):
    """Analyze numeric column"""
    return {
        "count": int(col.count()),
        "mean": round(float(col.mean()), 2) if col.count() > 0 else None,
        "median": round(float(col.median()), 2) if col.count() > 0 else None,
        "std": round(float(col.std()), 2) if col.count() > 0 else None,
        "min": float(col.min()) if col.count() > 0 else None,
        "max": float(col.max()) if col.count() > 0 else None
    }

def analyze_categorical_column(col):
    """Analyze categorical column"""
    counts = col.value_counts(dropna=True)
    percentages = round((counts / col.count()) * 100, 2)
    summary = pd.DataFrame({"Count": counts, "Percentage": percentages})
    return summary

def analyze_column(df, column_name):
    """
    Analyze a single column and return structured dict for display, export, and charting.
    """
    if column_name not in df.columns:
        return {"error": f"Column '{column_name}' does not exist."}

    col = df[column_name]

    # Try converting to numeric
    col_numeric = pd.to_numeric(col, errors='coerce')

    # Treat as numeric if there are numeric values
    if col_numeric.notna().sum() > 0:
        summary = analyze_numeric_column(col_numeric)
        return {
            "type": "numeric",
            "column": column_name,
            "summary": summary
        }
    else:
        # Categorical
        counts = col.value_counts(dropna=True)
        summary_dict = counts.to_dict()
        top_values = dict(list(counts.items())[:5])
        return {
            "type": "categorical",
            "column": column_name,
            "unique_values": int(col.nunique()),
            "summary": summary_dict,
            "top_values": top_values
        }