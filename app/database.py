import os
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URI)
db = client.nikata_test

async def find_user(user_name: str):
    return await db.users.find_one({ "name": user_name })
