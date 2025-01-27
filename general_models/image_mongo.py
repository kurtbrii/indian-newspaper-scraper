from pydantic import BaseModel
from datetime import datetime


class MongoImage(BaseModel):
    image: str
    image_name: str
    website: str
    platform: str
    date_created: datetime
    date_updated: datetime
    visited: bool
