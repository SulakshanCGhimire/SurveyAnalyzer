import matplotlib
matplotlib.use("Agg")  # non-GUI backend for server
import matplotlib.pyplot as plt
import os

def generate_numeric_chart(df, column_name, output_dir="charts"):
    """
    Generate a histogram for a numeric column
    """
    if column_name not in df.columns:
        return None

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{column_name}_hist.png")

    plt.figure(figsize=(6,4))
    df[column_name].dropna().hist(bins=20, color="skyblue", edgecolor="black")
    plt.title(f"{column_name} Histogram")
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    return file_path

def generate_categorical_chart(df, column_name, output_dir="charts"):
    """
    Generate a bar chart for top 5 categorical values
    """
    if column_name not in df.columns:
        return None

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{column_name}_bar.png")

    counts = df[column_name].value_counts().head(5)
    plt.figure(figsize=(6,4))
    counts.plot(kind="bar", color="orange", edgecolor="black")
    plt.title(f"{column_name} Top 5 Values")
    plt.xlabel(column_name)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    return file_path