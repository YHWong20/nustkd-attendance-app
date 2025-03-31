from flask import Flask, render_template, request, jsonify
from src.database import add_entry

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


if __name__ == "__main__":
    app.run(debug=True)
