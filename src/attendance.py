from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from member import Member
import json
import sys

# ATTENDANCE = {}
today = datetime.today().day
JSON_PATH = "local/attendance.json"

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://wongyihao2000:8P3Q67Vz82BmZ1ju@nustkd-attendance.7xhbpc4.mongodb.net/?retryWrites=true&w=majority&appName=nustkd-attendance"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    sys.exit(1)

db = client["attendance-dev"]
collection = db[str(today)]  # A collection for each training date


def add(name, status):
    member = Member(name, status)

    entry = {
        "_id": member.member_id,
        "name": member.name,
        "status": member.status,
    }

    try:
        collection.insert_one(entry)
        print(f"Key {entry['_id']} added!")
    except DuplicateKeyError:
        print(f"Duplicate key {entry['_id']} entered - ignoring...")
