"""
Google drive utilities
"""

import json
import os
from datetime import datetime, timezone, timedelta
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Save json credentials locally
SERVICE_ACCOUNT_JSON = os.environ["SERVICE_ACCOUNT_JSON"]
creds = json.loads(SERVICE_ACCOUNT_JSON, strict=False)
creds["private_key"] = creds.get("private_key").encode().decode("unicode-escape")
with open("creds.json", "w", encoding="utf-8") as jsonfile:
    json.dump(creds, jsonfile)

# Authenticate to google drive
settings = {
    "client_config_backend": "service",
    "service_config": {"client_json_file_path": "creds.json"},
}

gauth = GoogleAuth(settings=settings)
gauth.ServiceAuth()
drive = GoogleDrive(gauth)


def get_file():
    """
    Get attendance file for the current month.

    Returns:
        (int, str): Tuple of attendance file id and file name
    """
    # Get attendance sheet file id for current month
    sgt = timezone(timedelta(hours=8))
    month = datetime.now(sgt).strftime("%b")
    year = datetime.now(sgt).strftime("%y")
    title = f"{month}{year}_Attendance_Taekwondo.xlsx"

    # Query google drive for file id
    query = {"q": f"title='{title}'"}
    files = drive.ListFile(query).GetList()

    return (files[0]["id"], title)


def download_file():
    """
    Download file to local machine from google drive.

    Returns:
        str: Local file path for downloaded file.
    """
    (file_id, title) = get_file()
    local_path = f"local_{title}"

    f = drive.CreateFile({"id": file_id})
    f.GetContentFile(local_path)
    print("File downloaded from google drive.")

    return local_path


def upload_file():
    """
    Upload local file to google drive.
    """
    (file_id, title) = get_file()
    local_path = f"local_{title}"

    f = drive.CreateFile({"id": file_id})
    f.SetContentFile(local_path)
    f.Upload()
    print("File uploaded to google drive.")
