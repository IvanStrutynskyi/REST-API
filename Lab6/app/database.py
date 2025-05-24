import motor.motor_asyncio
from .config import MONGO_DETAILS, DATABASE_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client[DATABASE_NAME]
book_collection = database["books"]
