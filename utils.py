from json import load
import os
import requests
from datetime import datetime, timezone


def load_file(file_name) -> dict:
    with open(file_name, "r") as f:
        return load(f)


def download_images(image_src, folder_path, publication_name, publication_date, count):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    response = requests.get(image_src)
    with open(
        f"{folder_path}/{publication_name} {publication_date} {count}.jpg", "wb"
    ) as file:
        file.write(response.content)
    print("Image downloaded successfully!")


def image_dictionary(image_src, date, counter, platform, website_name) -> dict:
    return {
        "image": image_src,
        "image_name": f"{platform} {date} {counter}",
        "date_created": datetime.now(timezone.utc),
        "date_updated": datetime.now(timezone.utc),
        "website": website_name,
        "platform": platform,
        "visited": True,
    }
