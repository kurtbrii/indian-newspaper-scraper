from playwright.sync_api import sync_playwright, Page, BrowserContext
import time
from utils import download_images, image_dictionary
from general_models.mongodb_client import MongoDBClient
from general_models.image_mongo import MongoImage


class Prajasakti:

    def scrape_website(self, url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # ! main page
            page = context.new_page()
            page.goto(url)

            # ! open each newspaper
            # if newsper type == 0: main; if 1: districts
            database_name = "prajasakti"
            mongodb_client = MongoDBClient(database_name, "temporary")
            self.scrape_all(page, 0, context, mongodb_client, url, "main")
            self.scrape_all(page, 1, context, mongodb_client, url, "district")

            time.sleep(1)
            browser.close()

    def scrape_all(
        self,
        page: Page,
        newspaper_type,
        context: BrowserContext,  # for opening a new browser
        mongodb_client: MongoDBClient,
        url: str,
        type: str,
    ):
        newspapers = self.newspaper_locator(page, newspaper_type)
        mongodb_client.collection = mongodb_client.database[type]

        # TODO: opening in new tab instead of front and back
        # ! loop each news paper
        for newspaper_index in range(newspapers.count()):
            newspaper_name = (
                newspapers.locator(".card-body.edition-bg.card-text")
                .nth(newspaper_index)
                .text_content()
            ).strip()

            newspapers.nth(newspaper_index).click()

            # ! loop each page of the current newspaper
            page_number = 1
            next_button = page.locator(".bi.bi-caret-right-fill")
            while next_button.is_visible():
                self.each_page(
                    page, page_number, newspaper_name, url, mongodb_client, type
                )
                next_button.click()
                page_number += 1
            self.each_page(page, page_number, newspaper_name, url, mongodb_client, type)

            # after downloading the images and putting in mongoDB, go back to the original pagek
            page.goto(url)

    def each_page(
        self,
        page: Page,
        page_number: int,
        newspaper_name: str,
        url: str,
        mongodb_client: MongoDBClient,
        type: str,
    ):
        image_source = page.locator("#epaper").nth(1).get_attribute("src")
        publication_date = page.locator("#date").get_attribute("value")

        date_split = publication_date.split("-")
        date_split[0] = date_split[0][2:]

        new_publication_date = f"{date_split[1]}-{date_split[2]}-{date_split[0]}"

        download_images(
            f"{url}/{image_source}",
            f"prajasakti/{type}/{newspaper_name}",
            newspaper_name.upper(),
            new_publication_date,
            page_number,
        )

        image_dict = image_dictionary(
            f"{url}{image_source}",
            publication_date,
            page_number,
            newspaper_name.upper(),
        )
        image_instance = MongoImage(**image_dict)
        mongodb_client.insert_image(image_instance.model_dump())

    def newspaper_locator(self, page: Page, newspaper_type: int):
        newspapers = (
            page.locator(".row.row-custom")
            .nth(newspaper_type)
            .locator(".col-6.col-lg-3.col-custom")
        )

        return newspapers
