"""
MongoDB Database utilities
"""

import os
from datetime import datetime, timezone, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from src.member import Member

MONGO_URI = os.environ["MONGODB_URI"]
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
except Exception as e:
    print(e)

db = client["attendance-prod"]


def get_db_collection():
    """
    Get MongoDB collection for the current training day.

    Returns:
        Collection: MongoDB collection for the current training day.
    """
    # Get current day
    sgt = timezone(timedelta(hours=8))
    today = datetime.now(sgt).day

    # Collection for today's training date
    collection = db[str(today)]
    return collection


def add_entry(name, status):
    """
    Add entry to DB.

    Args:
        name (str): Member name.
        status (str): Member status.
    """
    collection = get_db_collection()
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


def get_entries(collection_name):
    """
    Get entries from DB.

    Args:
        collection_name (str): Collection to retrieve.

    Returns:
        list: List of entries in collection.
    """
    get_collection = db[collection_name]
    cursor = get_collection.find({})
    results = []
    for doc in cursor:
        results.append(doc)

    return results
