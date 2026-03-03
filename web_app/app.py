from flask import Flask, render_template, request
import os
from flask import send_from_directory

from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column
from survey_analyzer.visualizer import generate_numeric_chart, generate_categorical_chart

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
# Routes
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    txt_file = export_txt_report(result, selected_column, output_dir) if request.form.get("export") else None

    if df is None:
        return "Dataset could not be loaded. Check the CSV path!"

    columns = df.columns.tolist()
    result = None
    chart_filename = None

    if request.method == "POST":
        selected_column = request.form.get("column")

        if selected_column:
            result = analyze_column(df, selected_column)

            # Directory where charts are saved (absolute disk path)
            charts_dir = os.path.join(app.static_folder, "charts")

            if result["type"] == "numeric":
                saved_path = generate_numeric_chart(df, selected_column, charts_dir)
            elif result["type"] == "categorical":
                saved_path = generate_categorical_chart(df, selected_column, charts_dir)
            else:
                saved_path = None

            # Extract ONLY filename (important!)
            if saved_path:
                chart_filename = os.path.basename(saved_path)
        
        if request.form.get("export"):  # A button named 'export' in the form
            output_dir = os.path.join(app.static_folder, "exports")
            txt_file = export_txt_report(result, selected_column, output_dir)
        # You can pass this to the template for download links

    return render_template(
        "index.html",
        columns=columns,
        result=result,
        chart_filename=chart_filename,
        txt_file=txt_file if request.form.get("export") else None
    )
def download_file(filename):
    """
    Serve files from the output/ folder for download.
    """
    return send_from_directory(output_dir, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)