"""
Google drive utilities
"""

import json
import logging
import os
from datetime import datetime, timezone, timedelta
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)8s: %(message)s"
)

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

    try:
        # Query google drive for file id
        query = {"q": f"title='{title}'"}
        files = drive.ListFile(query).GetList()

        if not files:
            logging.error("File %s not found.", title)
            raise FileNotFoundError(f"File {title} not found in Google Drive.")

        file_id = files[0]["id"]
        logging.info("File %s found. File id: %s", title, file_id)
        return (file_id, title)
    except Exception as e:
        logging.error("Failed to get file from Google Drive. Error: %s", e)
        raise e


def download_file():
    """
    Download file to local machine from google drive.

    Returns:
        str: Local file path for downloaded file.
    """
    (file_id, title) = get_file()
    local_path = f"local_{title}"

    try:
        f = drive.CreateFile({"id": file_id})
        f.GetContentFile(local_path)
        logging.info("File downloaded from Google Drive.")
        return local_path
    except Exception as e:
        logging.error("Failed to download file from Google Drive. Error: %s", e)
        raise e


def upload_file():
    """
    Upload local file to google drive.
    """
    (file_id, title) = get_file()
    local_path = f"local_{title}"

    try:
        f = drive.CreateFile({"id": file_id})
        f.SetContentFile(local_path)
        f.Upload()
        logging.info("File uploaded to Google Drive.")
    except Exception as e:
        logging.error("Failed to upload file to Google Drive. Error: %s", e)
        raise e
