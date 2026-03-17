import csv
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "https://www.ebay.com/globaldeals/tech"
CSV_FILE = "ebay_tech_deals.csv"
FIELDNAMES = ["timestamp", "title", "price", "original_price", "shipping", "item_url"]


def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    return driver


def scroll_to_bottom(driver):
    """Scroll down repeatedly to trigger lazy loading."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_text(element, selector):
    try:
        return element.find_element(By.CSS_SELECTOR, selector).text.strip()
    except Exception:
        return "N/A"


def get_attr(element, selector, attr):
    try:
        return element.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
    except Exception:
        return "N/A"


def scrape():
    driver = init_driver()
    driver.get(URL)
    time.sleep(3)
    scroll_to_bottom(driver)

    products = driver.find_elements(By.CSS_SELECTOR, "div.dne-itemtile-detail")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []

    for p in products:
        title         = get_text(p, "h3.dne-itemtile-title")
        price         = get_text(p, "span.first")
        original_price = get_text(p, "span.itemtile-price-strikethrough")
        shipping      = get_text(p, "span.dne-itemtile-shipping")
        try:
            item_url = p.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
        except Exception:
            item_url = "N/A"

        rows.append({
            "timestamp":      timestamp,
            "title":          title,
            "price":          price,
            "original_price": original_price,
            "shipping":       shipping,
            "item_url":       item_url,
        })

    driver.quit()

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

    print(f"[{timestamp}] Scraped {len(rows)} products.")


if __name__ == "__main__":
    scrape()
