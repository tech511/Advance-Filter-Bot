from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["AutoFilterBot"]

# Start Image collection
start_images = db.start_images

def save_start_image(file_id: str):
    start_images.update_one({"_id": "start_image"}, {"$set": {"file_id": file_id}}, upsert=True)

def get_start_image():
    data = start_images.find_one({"_id": "start_image"})
    return data["file_id"] if data else None
