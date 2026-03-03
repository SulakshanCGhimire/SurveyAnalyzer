import os

def export_txt_report(result, column, output_dir):
    """
    Generates a TXT report for a given analysis result.
    
    Parameters:
    - result: dict returned by analyze_column()
    - column: name of the analyzed column
    - output_dir: directory to save TXT report
    """
    # File name
    filename = f"{column}_analysis.txt"
    path = os.path.join(output_dir, filename)

    # Write report
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Analysis Report for Column: {column}\n")
        f.write("="*50 + "\n\n")

        if result["type"] == "numeric":
            stats = result["summary"]
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
        elif result["type"] == "categorical":
            counts = result["summary"]
            for k, v in counts.items():
                f.write(f"{k}: {v}\n")
        else:
            f.write("No summary available.\n")

    # Return the filename for download or reference
    return filename