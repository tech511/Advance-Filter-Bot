from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI

client = AsyncIOMotorClient(DATABASE_URI)
db = client["AutoFilterBot"]

files = db["files"]
settings = db["settings"]
manual_filters = db["manual_filters"]

async def save_file(name, file_id):
    await files.insert_one({"name": name.lower(), "file_id": file_id})

async def search_file(query):
    return await files.find_one({"name": {"$regex": query.lower()}})

async def add_manual_filter(keyword, reply):
    await manual_filters.insert_one({"keyword": keyword.lower(), "reply": reply})

async def check_manual_filter(text):
    return await manual_filters.find_one({"keyword": text.lower()})

async def set_start_image(file_id):
    await settings.update_one(
        {"_id": "start_image"},
        {"$set": {"file_id": file_id}},
        upsert=True
    )

async def get_start_image():
    data = await settings.find_one({"_id": "start_image"})
    return data["file_id"] if data else None
