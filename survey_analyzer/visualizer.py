import matplotlib
matplotlib.use("Agg")  # non-GUI backend for server
import matplotlib.pyplot as plt
import os

def generate_numeric_chart(df, column_name, charts_dir):
    """
    Generate a histogram for a numeric column and save it to charts_dir.
    Returns the full path to the saved chart.
    """
    if column_name not in df.columns:
        return None

    os.makedirs(charts_dir, exist_ok=True)

    # File name with proper safe path
    file_path = os.path.join(charts_dir, f"{column_name}_hist.png")

    # Create figure
    plt.figure(figsize=(6,4))
    df[column_name].dropna().hist(bins=20, color="skyblue", edgecolor="black")
    plt.title(f"{column_name} Histogram")
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.tight_layout()

    # Save figure
    plt.savefig(file_path)
    plt.close()  # free memory

    return file_path

def generate_categorical_chart(df, column_name, charts_dir):
    """
    Generate a bar chart for top 5 categorical values and save it to charts_dir.
    Returns the full path to the saved chart.
    """
    if column_name not in df.columns:
        return None

    os.makedirs(charts_dir, exist_ok=True)
    file_path = os.path.join(charts_dir, f"{column_name}_bar.png")

    counts = df[column_name].value_counts().head(5)
    plt.figure(figsize=(6,4))
    counts.plot(kind="bar", color="orange", edgecolor="black")
    plt.title(f"{column_name} Top 5 Values")
    plt.xlabel(column_name)
    plt.ylabel("Count")
    plt.tight_layout()

    # Save figure
    plt.savefig(file_path)
    plt.close()

    return file_path