from constants import SINGLE_RUN
from general_models.redis_client import RedisClient

if __name__ == "__main__":
    redis_client = RedisClient()
    while True:
        redis_client.consume_website_url()

        if SINGLE_RUN:
            break
