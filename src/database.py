"""
MongoDB Database utilities
"""

import os
import logging
from datetime import datetime, timezone, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from src.member import Member

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)8s: %(message)s"
)

MONGO_URI = os.environ["MONGODB_URI"]
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
except Exception as e:
    logging.error("Failed to connect to MongoDB. Error: %s", e)
    raise e

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

    try:
        # Collection for today's training date
        collection = db[str(today)]
        logging.info("Retrieved collection for day %s.", str(today))
        return collection
    except Exception as e:
        logging.error("Failed to retrieve collection. Error: %s", e)
        raise e


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
        logging.info("Key %s added!", response.inserted_id)
    except DuplicateKeyError:
        logging.warning("Duplicate key %s entered - ignoring...", entry["_id"])
    except Exception as e:
        logging.error("Failed to add entry. Error: %s", e)
        raise e


def get_entries(collection_name):
    """
    Get entries from DB.

    Args:
        collection_name (str): Collection to retrieve.

    Returns:
        list: List of entries in collection.
    """
    try:
        get_collection = db[collection_name]
        cursor = get_collection.find({})
        results = []
        for doc in cursor:
            results.append(doc)

        logging.info(
            "Retrieved %s entries from collection %s.",
            len(results),
            collection_name
        )
        return results
    except Exception as e:
        logging.error(
            "Failed to get entries from collection %s. Error: %s",
            collection_name,
            e
        )
        raise e
