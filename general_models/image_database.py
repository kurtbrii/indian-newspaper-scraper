import boto3
from constants import KEY_ID, SECRET_KEY
import requests


class Boto3DB:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=KEY_ID,  # AWS_ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_KEY,  # AWS_SECRET_ACCESS_KEY,
            endpoint_url="https://minio-api.seven-gen.net/",  # AWS_ENDPOINT_URL,
        )

    def upload_image(self, image_url, publication_name, publication_date, count):
        response = requests.get(image_url)
        self.client.put_object(
            Bucket="newspapers",
            Key=f"{publication_name} {publication_date} {count}",
            Body=response.content,
            ContentType="image/jpeg",
        )
