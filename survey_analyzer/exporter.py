import os
import pandas as pd

def export_txt_report(result, column, output_dir):
    """
    Generates a TXT report for a given analysis result.
    
    Parameters:
    - result: dict returned by analyze_column()
    - column: name of the analyzed column
    - output_dir: directory to save TXT report
    Returns:
    - filename (str): name of the TXT file
    """
    # Ensure folder exists
    os.makedirs(output_dir, exist_ok=True)

    # File path
    filename = f"{column}_analysis.txt"
    path = os.path.join(output_dir, filename)

    # Write report
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Analysis Report for Column: {column}\n")
        f.write("="*50 + "\n\n")

        if result["type"] == "numeric":
            stats = result.get("summary", {})
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
        elif result["type"] == "categorical":
            counts = result.get("summary", {})
            for k, v in counts.items():
                f.write(f"{k}: {v}\n")
        else:
            f.write("No summary available.\n")

    return filename


def export_csv_summary(result, column, output_dir):
    """
    Export a CSV summary of the column analysis (numeric or categorical).
    
    Returns the filename for download.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{column}_summary.csv"
    path = os.path.join(output_dir, filename)

    if result["type"] == "numeric":
        # Convert summary dict to single-row DataFrame
        df = pd.DataFrame([result.get("summary", {})])
    elif result["type"] == "categorical":
        # Convert counts dict to DataFrame
        summary = result.get("summary", {})
        df = pd.DataFrame(list(summary.items()), columns=[column, "Count"])
    else:
        df = pd.DataFrame()

    df.to_csv(path, index=False)
    return filename