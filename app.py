from flask import Flask, render_template, request, jsonify
from src.database import add_entry, get_entries
# from src.export import insert_entries

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name")
    status = data.get("status")

    if not name or not status:
        return jsonify({"error": "Name and status must be provided"}), 400

    add_entry(name, status)
    return jsonify({"message": "Attendance recorded successfully"}), 200


@app.route("/export", methods=["GET"])
def export():
    if "date" not in request.args:
        return render_template("export.html")

    # Disabled for prod..
    # export_date = request.args.get('date')
    # entries = get_entries(export_date)

    # insert_entries(export_date, entries)

    return jsonify({"message": "Export started successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
