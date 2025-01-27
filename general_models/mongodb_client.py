from pymongo import MongoClient
from constants import CONNECTION_URL


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(CONNECTION_URL)
        self.database = self.client["newspapers"]
        self.collection = self.database["newspaper_collection"]

    def insert_image(self, images_dict: dict):
        self.collection.update_one(
            filter={
                "image": images_dict["image"],
            },
            update={"$setOnInsert": images_dict},
            upsert=True,
        )
