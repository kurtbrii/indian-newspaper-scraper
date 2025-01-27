from playwright.sync_api import sync_playwright, Page, BrowserContext
import time
from utils import download_images, image_dictionary
from general_models.mongodb_client import MongoDBClient
from general_models.image_database import Boto3DB
from general_models.image_mongo import MongoImage


class Siasat:
    def scrape_website(self, url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # ! main page
            page = context.new_page()
            page.goto(url)

            page.get_by_alt_text("Siasat Daily").click()

            counter = 0
            page.wait_for_event("load")
            newspaper_page = page.query_selector_all("#page-thumbs a")
            next_button = page.locator(".btn.btn-default.nextpage")
            # ! each page
            mongodb_client = MongoDBClient()
            boto3_client = Boto3DB()
            while counter <= len(newspaper_page):
                next_button.click()

                image_source = page.locator("#left-chunk-0 > img").get_attribute("src")

                date = page.locator("#calendar-menu > .dropdown-toggle").text_content()
                date_split = date.split(" ")
                publication_date = f"{date_split[2]}-{date_split[1]}-{date_split[3]}"

                image_dict = image_dictionary(
                    image_source,
                    publication_date,
                    counter + 1,
                    "SIASAT",
                    "SIASAT",
                )

                print(image_dict)
                image_instance = MongoImage(**image_dict)

                mongodb_client.insert_image(image_instance.model_dump())

                boto3_client.upload_image(
                    image_source,
                    "SIASAT",
                    publication_date,
                    counter + 1,
                )
                counter += 1

            time.sleep(3)
            browser.close()
