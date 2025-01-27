from playwright.sync_api import sync_playwright
from utils import download_images, image_dictionary
from general_models.mongodb_client import MongoDBClient
from general_models.image_mongo import MongoImage
from general_models.image_database import Boto3DB
import time


class Eenadu:
    def scrape_website(self, url: str):

        start_time = time.time()
        # opens browser, then navigates to the main page
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # to open browser

            page = browser.new_page()
            page.goto(url)

            # navigatesto the first newspaper
            newspapers = page.locator(".ep_ed_pg")
            newspaper_len = len(newspapers.all())

            mongodb_client = MongoDBClient()
            boto3_client = Boto3DB()
            for index in range(newspaper_len):
                # opens the newspaper in new tab so that the main page is preserved
                edate = page.locator(".ep_ed_img").nth(index).get_attribute("edate")
                eid = page.locator(".ep_ed_img").nth(index).get_attribute("eid")

                new_page = browser.new_page()
                new_page.goto(f"{url}/Home/Index?date={edate}&eid={eid}")

                owl_items = new_page.query_selector_all(".owl-item")
                next_button = new_page.locator(".owl-next")

                publication_name = page.locator(".ep_ed_title").nth(index).inner_text()
                date_published = new_page.locator("#datepicker").inner_text()
                # TODO: easier implementation: selector class --> .fas.fa-arrow-right (next button)
                next_button = new_page.locator(".fas.fa-arrow-right").first
                for page_number in range(len(owl_items)):

                    image_src = new_page.locator("#imgmain1").get_attribute("src")
                    image_src2 = new_page.locator("#imgmain2").get_attribute("src")

                    image_dict = image_dictionary(
                        image_src,
                        date_published,
                        page_number + 1,
                        publication_name.upper(),
                        "EENADU",
                    )

                    image_dict2 = image_dictionary(
                        image_src2,
                        date_published,
                        page_number + 1,
                        publication_name.upper(),
                        "EENADU",
                    )

                    image_instance = MongoImage(**image_dict)
                    mongodb_client.insert_image(image_instance.model_dump())

                    image_instance2 = MongoImage(**image_dict2)
                    mongodb_client.insert_image(image_instance2.model_dump())

                    # ! image upload
                    boto3_client.upload_image(
                        image_src, "EENADU", date_published, page_number + 1
                    )

                    boto3_client.upload_image(
                        image_src2,
                        "EENADU",
                        date_published,
                        f"{page_number + 1} (1)",
                    )

                    # download_images(
                    #     image_src,
                    #     f"eenadu/{publication_name}",
                    #     publication_name,
                    #     date_published,
                    #     page_number + 1,
                    # )

                    # download_images(
                    #     image_src2,
                    #     f"eenadu/{publication_name}",
                    #     publication_name,
                    #     date_published,
                    #     f"{page_number + 1} (1)",
                    # )

                    next_button.click()

            browser.close()

        end_time = time.time()

        total_time = end_time - start_time

        print(f"{total_time} seconds per {newspaper_len} newspapers")
