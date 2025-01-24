from playwright.async_api import async_playwright
import time
import requests
import os


class AndhraJyotiScraper:
    async def download_image(self, date, eid, owl_items, img_locator) -> list:
        folder_path = f"{eid}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        images = []
        for index in range(len(owl_items)):
            img_src = await img_locator.nth(index).get_attribute("highres")
            if img_src:
                response = requests.get(img_src)
                with open(f"{folder_path}/{index}.jpg", "wb") as file:
                    file.write(response.content)
                images.append(img_src)
                print("Image downloaded successfully!")
        print("=======")
        return images

    async def scrape_website(self, url: str):
        async with async_playwright() as p:
            # opens browser, then navigates to the main page
            browser = await p.chromium.launch(headless=False)  # to open browser

            page = await browser.new_page()
            await page.goto(url)

            # navigatesto the first newspaper
            newspapers = page.locator(".ep_ed_pg")
            newspaper_len = len(await newspapers.all())

            for index in range(newspaper_len):
                # opens the newspaper in new tab so that the main page is preserved
                edate = (
                    await page.locator(".ep_ed_img").nth(index).get_attribute("edate")
                )
                eid = await page.locator(".ep_ed_img").nth(index).get_attribute("eid")

                new_page = await browser.new_page()
                await new_page.goto(f"{url}/Home/Index?date={edate}&eid={eid}")

                # owl-item = specific/each page of the newspaper
                await new_page.wait_for_selector(".owl-item")
                owl_items = await new_page.query_selector_all(".owl-item")
                img_locator = new_page.locator("div.item img")

                # download images
                # images = await self.download_image(edate, index, owl_items, img_locator)

            time.sleep(3)
            await browser.close()
