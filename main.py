import os
import json
import time
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from scrapers.amazon import AmazonScraper
from scrapers.shopify import ShopifyScraper

# Load configuration
load_dotenv()

def send_alert(product_name, current_price, target_price, url):
    """Sends a professional notification via email."""
    msg = EmailMessage()
    msg.set_content(f"""
    Market Alert: Price Drop Detected!

    Product: {product_name}
    Current Price: {current_price:.2f}
    Target Price: {target_price:.2f}
    Link: {url}

    This alert was generated automatically by your E-commerce Intelligence Suite.
    """)

    msg['Subject'] = f"PRICE DROP: {product_name} is now {current_price:.2f}"

    msg['From'] = os.getenv("SMTP_EMAIL")
    msg['To'] = os.getenv("SMTP_EMAIL") 

    try:
        with smtplib.SMTP(os.getenv("SMTP_ADDRESS"), 587) as server:
            server.starttls()
            server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
            server.send_message(msg)
            print(f"Alert/Email sent for {product_name}")
    except Exception as e:
        print(f"ERROR: Failed to send email alert: {e}")


def main():
    print("--- Starting price check ---")
    
    # Load products to monitor
    try:
        with open("products.json", "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        print("Error: products.json not found.")
        return

    # Use a single driver instance for the session to be more efficient
    amazon_scraper = AmazonScraper()
    shopify_scraper = ShopifyScraper()

    for product in products:
        name = product["name"]
        url = product["url"]
        target = product["target_price"]
        platform = product["platform"]

        print(f"Checking {platform.capitalize()} - {name}...")
        
        current_price = None
        if platform == "amazon":
            current_price = amazon_scraper.get_price(url)
        elif platform == "shopify":
            current_price = shopify_scraper.get_price(url)
        else:
            print(f"Skipping {name}: Platform '{platform}' not yet supported.")
            continue

        if current_price:
            print(f"Current Price: {current_price:.2f} (Target: {target:.2f})")
            if current_price <= target:
                send_alert(name, current_price, target, url)
        else:
            print(f"FAILED: Could not extract price for {name}.")

        # Human-like delay between product checks
        time.sleep(random.uniform(5, 10))
    
    amazon_scraper.close()
    shopify_scraper.close()

if __name__ == "__main__":
    main()
