from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

users_collection = db["users"]  
products_collection = db["products"]
cart_collection = db["cart"]
orders_collection = db["orders"]
order_items_collection = db["order_items"]