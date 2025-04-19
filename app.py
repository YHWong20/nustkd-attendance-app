"""
Flask app entry point
"""

from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, jsonify
from src.database import add_entry, get_entries
from src.export import insert_entries
from src.telegram import send_message

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Index/Home page render function.

    Returns:
        Rendered HTML template.
    """
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    """
    Attendance submission function.

    Returns:
        JSON Message and HTTP Status Code.
    """
    data = request.get_json()
    name = data.get("name")
    status = data.get("status")

    if not name or not status:
        return jsonify({"error": "Name and status must be provided"}), 400

    add_entry(name, status)
    return jsonify({"message": "Attendance recorded successfully"}), 200


@app.route("/export", methods=["GET"])
def export():
    """
    Attendance export page render function.

    Returns:
        If export date not provided - Rendered HTML template.
        If export date is provided - JSON Message and HTTP Status Code.
    """
    if "date" not in request.args:
        return render_template("export.html")

    export_date = request.args.get("date")
    entries = get_entries(export_date)

    # Get current date
    sgt = timezone(timedelta(hours=8))
    current_day = datetime.now(sgt).day
    current_month = datetime.now(sgt).month
    day_month = f"{current_day}/{current_month}"

    telegram_bit = request.args.get("telegram")
    if int(telegram_bit) == 1:
        # Export attendance list to Telegram
        send_message(day_month, entries)
    else:
        # Export attendance list to Excel sheet
        insert_entries(export_date, entries)

    return jsonify({"message": "Export started successfully"}), 200


@app.route("/today", methods=["GET"])
def today():
    """
    Get Today's Attendance page render function.

    Returns:
        Rendered HTML template.
    """
    # Get current date
    sgt = timezone(timedelta(hours=8))
    current_day = datetime.now(sgt).day
    current_month = datetime.now(sgt).month
    day_month = f"{current_day}/{current_month}"

    entries = get_entries(str(current_day))
    _students = ""
    _alumni = ""
    _exchangers = ""

    for entry in entries:
        if entry["status"] == "Regular":
            _students += f"{entry['name']} <br>"
        elif entry["status"] == "Alumni":
            _alumni += f"{entry['name']} <br>"
        elif entry["status"] == "Exchange":
            _exchangers += f"{entry['name']} <br>"

    return render_template(
        "get.html",
        day_month=day_month,
        students=_students,
        alumni=_alumni,
        exchangers=_exchangers,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
