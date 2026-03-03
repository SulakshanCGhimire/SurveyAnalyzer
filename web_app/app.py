from unittest import result

from flask import Flask, render_template, request
import os
import sys

# Add project root to sys.path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column
from survey_analyzer.visualizer import generate_numeric_chart, generate_categorical_chart

app = Flask(__name__)

# Load dataset once at startup
df = load_dataset(os.path.join("data", "nepal_earthquake.csv"))

@app.route("/", methods=["GET", "POST"])
def index():
    if df is None:
        return "Dataset could not be loaded. Check the CSV path!"

    columns = df.columns.tolist()
    result = None
    chart_file = None
    columns = df.columns.tolist()
    result = None
    chart_file = None

    if request.method == "POST":
        selected_column = request.form.get("column")
        if selected_column:
            result = analyze_column(df, selected_column)

        charts_dir = os.path.join(project_root, "web_app", "static", "charts")
        if result["type"] == "numeric":
            chart_file = generate_numeric_chart(df, selected_column, charts_dir)
        elif result["type"] == "categorical":
            chart_file = generate_categorical_chart(df, selected_column, charts_dir)

        # Make path relative to static
        if chart_file:
            chart_file = os.path.relpath(chart_file, os.path.join(project_root, "web_app", "static"))
        return render_template("index.html", columns=columns, result=result, chart_file=chart_file)



if __name__ == "__main__":
    # This ensures Flask runs correctly when executed as a script
    app.run(debug=True)