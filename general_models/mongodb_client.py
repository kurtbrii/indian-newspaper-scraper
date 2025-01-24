from pymongo import MongoClient
from constants import CONNECTION_URL


class MongoDBClient:
    def __init__(self, database_name, collection_name):
        self.client = MongoClient(CONNECTION_URL)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def find_duplicate(self):
        pass

    def insert_image(self, images_dict: dict):
        self.collection.update_one(
            filter={
                "image": images_dict["image"],
            },
            update={"$setOnInsert": images_dict},
            upsert=True,
        )
