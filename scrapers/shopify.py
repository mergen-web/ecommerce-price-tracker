from .base import BaseScraper

class ShopifyScraper(BaseScraper):
    def get_price(self, url):
        # We still try the JSON endpoint first as it's fastest and hardest to block
        # If that fails, the BaseScraper will load the page in a real browser via Selenium
        soup = self.get_soup(url)
        if not soup:
            return None
            
        # Updated selector for Shopify based on your screenshot
        selectors = [
            "span.text-black",
            ".price__regular .price-item--regular",
            ".price-item--sale",
            ".product__price",
            "[data-product-price]",
            ".price"
        ]
        
        for s in selectors:
            elem = soup.select_one(s)
            if elem:
                try:
                    return float(elem.get_text().strip().replace("$", "").replace(",", ""))
                except: continue
        
        return None
