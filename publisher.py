from general_models.redis_client import RedisClient
from utils import load_file

if __name__ == "__main__":
    redis_client = RedisClient()
    url = load_file("./url.json")["url"]

    redis_client.publish_website_url(url)