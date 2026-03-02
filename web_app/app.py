from flask import Flask, render_template, request
from survey_analyzer.parser import load_dataset
from survey_analyzer.analyzer import analyze_column

app = Flask(__name__)

# Load dataset once at startup
df = load_dataset("data/nepal_earthquake.csv")  # Update path to your CSV

@app.route("/", methods=["GET", "POST"])
def index():
    columns = df.columns.tolist()
    result = None

    if request.method == "POST":
        selected_column = request.form.get("column")
        if selected_column:
            result = analyze_column(df, selected_column)

    return render_template("index.html", columns=columns, result=result)

if __name__ == "__main__":
    app.run(debug=True)