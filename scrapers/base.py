import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import random

class BaseScraper:
    def __init__(self):
        # Set up a stealth browser
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = uc.Chrome(options=options)

    def get_soup(self, url):
        try:
            self.driver.get(url)
            # Increased wait time significantly to ensure page fully renders
            time.sleep(random.uniform(5, 10)) 
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            
            # Status message
            print(f"Checking: {self.driver.title}")
            
            return soup
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def close(self):
        self.driver.quit()

    def get_price(self, url):
        raise NotImplementedError("Subclasses must implement get_price()")
