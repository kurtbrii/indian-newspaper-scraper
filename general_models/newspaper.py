from scraping_models.eenadu import Eenadu
from scraping_models.andhra_jyoti import AndhraJyotiScraper
from scraping_models.hindi_milap import HindiMilap
from scraping_models.prajasakti import Prajasakti
from scraping_models.siasat import Siasat
from scraping_models.vaartha import Vaartha
from constants import QUEUE_NAME


class Newspaper:
    @staticmethod
    def run_scraper():
        match QUEUE_NAME:
            case "HINDI_MILAP":
                return HindiMilap()
            case "ANDHRA_JYOTO":
                return AndhraJyotiScraper()
            case "EENADU":
                return Eenadu()
            case "PRAJASAKTI":
                return Prajasakti()
            case "SIASAT":
                return Siasat()
            case "VAARTHA":
                return Vaartha()

            case _:
                raise ValueError(f"Unknown QUEUE_NAME: {QUEUE_NAME}")
