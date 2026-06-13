from .base import BaseScraper

class AmazonScraper(BaseScraper):
    def get_price(self, url):
        soup = self.get_soup(url)
        if not soup:
            return None
        
        # Look for the container that holds the whole price
        whole_elem = soup.select_one(".a-price-whole")
        fraction_elem = soup.select_one(".a-price-fraction")
        
        if whole_elem:
            whole_text = whole_elem.get_text().strip().replace(".", "").replace(",", "")
            fraction_text = fraction_elem.get_text().strip() if fraction_elem else "00"
            
            # Combine them: "10" + "." + "37" -> "10.37"
            full_price_str = f"{whole_text}.{fraction_text}"
            
            # Clean string to keep only digits and the decimal point
            # This handles any currency symbol ($, EUR, £, etc.)
            clean_price_str = "".join([c for c in full_price_str if c.isdigit() or c == '.'])
            
            try:
                return float(clean_price_str)
            except ValueError:
                print(f"Could not convert price string '{full_price_str}' to float.")
                return None
        
        return None
