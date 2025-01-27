from playwright.sync_api import sync_playwright, Page, Locator
import time
from utils import download_images, image_dictionary
from general_models.mongodb_client import MongoDBClient
from general_models.image_mongo import MongoImage
from general_models.image_database import Boto3DB


class Vaartha:
    def scrape_website(self, url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # ! main page
            page = context.new_page()
            page.goto(url)

            # ! open each newspaper
            self.all_newspapers(page, url)

            time.sleep(3)
            browser.close()

    def all_newspapers(self, page: Page, url: str):
        newspapers = page.query_selector_all(".category-thumb-box")

        mongodb_client = MongoDBClient()
        boto3_client = Boto3DB()

        counter = 0
        while counter < len(newspapers):
            page.locator(".category-thumb-box").nth(counter).click()

            details = page.locator(".heading-h4.h4").inner_text().split("-")
            publisher_name = details[0].replace("Main", "").strip()

            date = details[1].strip().split()

            try:
                date_published = f"{date[1]}-{date[0]}-{date[2][2:]}"
            except:
                date_published = "invalid date"

            page_counter = 0
            all_pages = page.locator(".epaper-thumb-nav a").count()
            while page_counter < all_pages - 1:
                self.each_page(
                    page,
                    page_counter,
                    mongodb_client,
                    boto3_client,
                    publisher_name,
                    date_published,
                )

                page.locator(".page-link > .fas.fa-forward").first.click()
                page_counter += 1

            self.each_page(
                page,
                page_counter,
                mongodb_client,
                boto3_client,
                publisher_name,
                date_published,
            )

            counter += 1

            page.goto(url)

    def each_page(
        self,
        page: Page,
        counter: str,
        mongodb_client: MongoDBClient,
        boto3_client: Boto3DB,
        publisher_name: str,
        date_published: str,
    ):

        image_source = page.locator(".page-image > img").get_attribute("src")

        image_dict = image_dictionary(
            image_source,
            date_published,
            counter + 1,
            publisher_name.upper(),
            "VAARTHA",
        )
        image_instance = MongoImage(**image_dict)

        mongodb_client.insert_image(image_instance.model_dump())

        boto3_client.upload_image(
            image_source,
            publisher_name.upper(),
            date_published,
            counter + 1,
        )
