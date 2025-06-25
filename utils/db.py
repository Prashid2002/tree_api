from pymongo import MongoClient
import os

def get_db():
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    return client("user_db")
