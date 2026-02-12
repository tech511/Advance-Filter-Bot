from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["AutoFilterBot"]
images_col = db["start_images"]
filters_col = db["filters"]

def save_start_image(file_id: str):
    """Save or update start image in DB"""
    images_col.update_one({"_id": "start"}, {"$set": {"file_id": file_id}}, upsert=True)

def get_start_image():
    """Get current start image file_id"""
    doc = images_col.find_one({"_id": "start"})
    return doc["file_id"] if doc else None

def add_filter(keyword: str, response: str):
    filters_col.insert_one({"keyword": keyword.lower(), "response": response})

def get_filter(keyword: str):
    doc = filters_col.find_one({"keyword": keyword.lower()})
    return doc["response"] if doc else None
