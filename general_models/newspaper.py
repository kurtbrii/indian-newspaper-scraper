from scraping_models.eenadu import Eenadu
from scraping_models.andhra_jyoti import AndhraJyotiScraper
from scraping_models.hindi_milap import HindiMilap
from scraping_models.prajasakti import Prajasakti
from constants import QUEUE_NAME


class Newspaper:
    @staticmethod
    def create_scraper():
        match QUEUE_NAME:
            case "HINDI_MILAP":
                return HindiMilap()
            case "ANDHRA_JYOTO":
                return AndhraJyotiScraper()
            case "EENADU":
                return Eenadu()
            case "PRAJASAKTI":
                return Prajasakti()

            case _:
                raise ValueError(f"Unknown QUEUE_NAME: {QUEUE_NAME}")
