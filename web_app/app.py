from flask import Flask, render_template, request, send_from_directory
import os

from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column
from survey_analyzer.visualizer import generate_numeric_chart, generate_categorical_chart
from survey_analyzer.exporter import export_txt_report, export_csv_summary

app = Flask(__name__)

# -------------------------------------------------
# Define project root
# -------------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Full path to CSV
csv_path = os.path.join(project_root, "data", "nepal_earthquake.csv")
print("Loading CSV from:", csv_path)

df = load_dataset(csv_path)
districts = sorted(df["DISTRICT"].dropna().unique().tolist())

# -------------------------------------------------
# Directories for charts and exports
# -------------------------------------------------
charts_dir = os.path.join(app.static_folder, "charts")
exports_dir = os.path.join(app.static_folder, "exports")

os.makedirs(charts_dir, exist_ok=True)
os.makedirs(exports_dir, exist_ok=True)

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    columns = df.columns.tolist()
    result = None
    chart_filename = None
    txt_file = None
    csv_file = None
    selected_column = None
    selected_column2 = None
    selected_district = "All"
    filtered_df = df  # default = full dataset

    if request.method == "POST":
        selected_column = request.form.get("column")
        selected_column2 = request.form.get("column2")
        selected_district = request.form.get("district", "All")
        action = request.form.get("action")  # analyze or export

        # Apply district filter
        if selected_district != "All":
            filtered_df = df[df["DISTRICT"] == selected_district]
        
        if selected_column:
            # Comparison mode
            if selected_column2:
                result1 = analyze_column(filtered_df, selected_column)
                result2 = analyze_column(filtered_df, selected_column2)

                # Only numeric columns can be compared
                if result1.get("type") == "numeric" and result2.get("type") == "numeric":
                    result = {
                        "type": "comparison",
                        "column1": selected_column,
                        "column2": selected_column2,
                        "mean1": result1.get("mean", 0),
                        "mean2": result2.get("mean", 0),
                        "count1": result1.get("count", 0),
                        "count2": result2.get("count", 0)
                    }

                    # Generate charts for both columns
                    saved_path1 = generate_numeric_chart(filtered_df, selected_column, charts_dir)
                    saved_path2 = generate_numeric_chart(filtered_df, selected_column2, charts_dir)
                    chart_filename = [os.path.basename(saved_path1), os.path.basename(saved_path2)]

                else:
                    result = {
                        "type": "error",
                        "message": "Comparison only works for numeric columns."
                    }
                    chart_filename = None

            # Single column analysis
            else:
                result = analyze_column(filtered_df, selected_column)
                if result["type"] == "numeric":
                    saved_path = generate_numeric_chart(filtered_df, selected_column, charts_dir)
                elif result["type"] == "categorical":
                    saved_path = generate_categorical_chart(filtered_df, selected_column, charts_dir)
                else:
                    saved_path = None

                if saved_path:
                    chart_filename = [os.path.basename(saved_path)]

        # Handle export if requested
        if action == "export" and result:
            txt_file = export_txt_report(result, selected_column, exports_dir)
            csv_file = export_csv_summary(result, selected_column, exports_dir)

        # Always render template (move outside 'if selected_column')
        return render_template(
            "index.html",
            columns=columns,
            selected_column=selected_column,
            selected_column2=selected_column2,
            districts=districts,
            selected_district=selected_district,
            result=result,
            chart_filename=chart_filename,
            txt_file=txt_file,
            csv_file=csv_file
        )

# -------------------------------------------------
# Serve files from exports folder
# -------------------------------------------------
@app.route("/exports/<filename>")
def download_file(filename):
    return send_from_directory(exports_dir, filename, as_attachment=True)

# -------------------------------------------------
# Run app
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)