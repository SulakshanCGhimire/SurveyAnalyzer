from flask import Flask, render_template, request, send_from_directory
import os

from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column
from survey_analyzer.visualizer import generate_numeric_chart, generate_categorical_chart
from survey_analyzer.exporter import export_txt_report  # make sure this exists

app = Flask(__name__)

# -------------------------------------------------
# Define project root
# -------------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Full path to CSV
csv_path = os.path.join(project_root, "data", "nepal_earthquake.csv")
print("Loading CSV from:", csv_path)

df = load_dataset(csv_path)

# -------------------------------------------------
# Directories for charts and exports
# -------------------------------------------------
charts_dir = os.path.join(app.static_folder, "charts")
os.makedirs(charts_dir, exist_ok=True)

output_dir = os.path.join(app.static_folder, "exports")
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    columns = df.columns.tolist()
    result = None
    chart_filename = None
    txt_file = None

    if request.method == "POST":
        selected_column = request.form.get("column")
        export = request.form.get("export")  # will be set if user clicked Export button

        if selected_column:
            result = analyze_column(df, selected_column)

            # Generate chart
            if result["type"] == "numeric":
                saved_path = generate_numeric_chart(df, selected_column, charts_dir)
            elif result["type"] == "categorical":
                saved_path = generate_categorical_chart(df, selected_column, charts_dir)
            else:
                saved_path = None

            if saved_path:
                chart_filename = os.path.basename(saved_path)

            # Generate TXT report if Export button clicked
            if export:
                txt_file = export_txt_report(result, selected_column, output_dir)

    return render_template(
        "index.html",
        columns=columns,
        result=result,
        chart_filename=chart_filename,
        txt_file=txt_file
    )

# -------------------------------------------------
# Serve files from exports folder
# -------------------------------------------------
@app.route("/exports/<filename>")
def download_file(filename):
    """
    Serve files from the exports folder for download.
    """
    return send_from_directory(output_dir, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)