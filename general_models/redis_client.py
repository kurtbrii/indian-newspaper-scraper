from redis import Redis
from constants import REDIS_KEY
from constants import HOST, PORT
from general_models import newspaper
from general_models.newspaper import Newspaper
from general_models.mongodb_client import MongoDBClient

import asyncio


class RedisClient:
    def __init__(self):
        self.redis_client = Redis(
            host=HOST,
            port=int(PORT),
            decode_responses=True,
        )

    def publish_website_url(self, url: str):
        self.redis_client.sadd(REDIS_KEY, url)

    def consume_website_url(self):
        urls = self.redis_client.spop(REDIS_KEY, 5) or []
        for url in urls:
            general_newspaper = Newspaper.run_scraper()
            general_newspaper.scrape_website(url)
