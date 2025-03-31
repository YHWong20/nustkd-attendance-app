import os
import sys
from datetime import datetime, timezone, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from src.member import Member


sgt = timezone(timedelta(hours=8))
today = datetime.now(sgt).day
JSON_PATH = "local/attendance.json"

# Connect to MongoDB Atlas
MONGO_URI = os.environ['MONGODB_URI']
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    sys.exit(1)

db = client["attendance-dev"]
collection = db[str(today)]  # A collection for each training date


def add_entry(name, status):
    member = Member(name, status)

    entry = {
        "_id": member.member_id,
        "name": member.name,
        "status": member.status,
    }

    try:
        response = collection.insert_one(entry)
        assert response.acknowledged
        print(f"Key {response.inserted_id} added!")
    except DuplicateKeyError:
        print(f"Duplicate key {entry['_id']} entered - ignoring...")
