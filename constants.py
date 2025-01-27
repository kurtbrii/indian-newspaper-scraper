from dotenv import load_dotenv
import os

load_dotenv()

PORT = os.getenv("PORT", "")
HOST = os.getenv("HOST", "")
CONNECTION_URL = os.getenv("CONNECTION_URL", "")
REDIS_KEY = os.getenv("REDIS_KEY", "")
QUEUE_NAME = os.getenv("EENADU", "EENADU")
SINGLE_RUN = os.getenv("SINGLE_RUN", True)

# ! boto3 access
KEY_ID = os.getenv(
    "KEY_ID",
    "HSYS7o1I8mS0IZwtCdB8",
)
SECRET_KEY = os.getenv("SECRET_KEY", "MDS971A1wm1qeaNyQ93CokgMr7t5zN4dC7WVGxhO")

# Publication Name MM-DD-YY-Page.
