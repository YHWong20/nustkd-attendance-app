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

# Get attendance sheet file id for current month
sgt = timezone(timedelta(hours=8))
month = datetime.now(sgt).strftime("%b")
year = datetime.now(sgt).strftime("%y")
TITLE = f"{month}{year}_Attendance_Taekwondo.xlsx"
LOCAL_PATH = f"local_{TITLE}"

query = {"q": f"title='{TITLE}'"}
files = drive.ListFile(query).GetList()
file_id = files[0]["id"]


def download_file():
    """
    Download file to local machine from google drive.

    Returns:
        str: Local file path for downloaded file.
    """
    f = drive.CreateFile({"id": file_id})
    f.GetContentFile(LOCAL_PATH)
    print("File downloaded from google drive.")
    return LOCAL_PATH


def upload_file():
    """
    Upload local file to google drive.
    """
    f = drive.CreateFile({"id": file_id})
    f.SetContentFile(LOCAL_PATH)
    f.Upload()
    print("File uploaded to google drive.")
