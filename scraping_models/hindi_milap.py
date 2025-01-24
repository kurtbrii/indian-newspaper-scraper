from playwright.sync_api import sync_playwright
import time
from general_models.mongodb_client import MongoDBClient
from general_models.image_mongo import MongoImage
from datetime import datetime, timezone
from utils import download_images, image_dictionary


class HindiMilap:
    @staticmethod
    def date_splitter(date) -> str:
        date_split = date.split("-")
        date_split[-1] = date_split[-1][2:]
        date_string = "-".join(date_split)

        return date_string

    def test(self, new_page, mongodb_client, date, counter):
        time.sleep(1)
        image_selector = ".carousel-item.active > .parent-container > img"
        new_page.wait_for_selector(image_selector, state="attached", timeout=5000)
        image_src = new_page.locator(image_selector).last.get_attribute("src")

        image_dict = image_dictionary(image_src, date, counter, "HINDI_MILAP")
        # image_dict = {
        #     "image": image_src,
        #     "image_name": f"HINDI MILAP {date} {counter}",
        #     "date_created": datetime.now(timezone.utc),
        #     "date_updated": datetime.now(timezone.utc),
        #     "platform": "HINDI MILAP",
        #     "visited": True,
        # }
        image_instance = MongoImage(**image_dict)

        #! insert then download
        mongodb_client.insert_image(image_instance.model_dump())
        download_images(image_src, "hindi_milap", "HINDI MILAP", date, counter)

    def scrape_website(self, url):
        start_time = time.time()

        with sync_playwright() as p:
            #! opens browser and open the url
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)

            #! navigates to the actual page (actual page) after main page is fully
            with context.expect_page() as new_page_info:
                page.locator(".epaper-common-card-container").click()

                new_page = new_page_info.value

                # waits for it to load
                date_selector = "input[placeholder='Select Date']"
                date = str(new_page.locator(date_selector).get_attribute("value"))

                # clicking of next button
                selector = "button[aria-label='Next']"
                new_page.wait_for_selector(selector, state="attached", timeout=5000)
                next_button = new_page.locator(selector)

                # date splitter
                self.date_splitter(date)

                mongodb_client = MongoDBClient("hindi_milap", f"hindi_milap-{date}")
                counter = 1
                while next_button.count() > 0:
                    self.test(new_page, mongodb_client, date, counter)
                    next_button.last.click()
                    counter += 1

                self.test(new_page, mongodb_client, date)

            browser.close()

        end_time = time.time()
        total_time = end_time - start_time

        print(f"{total_time} seconds per one newspaper")
