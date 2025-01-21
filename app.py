import os
import re
import csv
import time  # Correctly importing time
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def parse_listing_data(name, details):
    """Parse listing details to extract price and date."""
    price_match = re.search(r"\$([0-9,]+)", details)
    if not price_match:
        return None, None
    price = float(price_match.group(1).replace(',', ''))

    date_match = re.search(r"on (\d{1,2}/\d{1,2}/\d{2})", details)
    if not date_match:
        return None, None

    date_str = date_match.group(1)
    try:
        date = datetime.strptime(date_str, "%m/%d/%y")
        formatted_date = date.strftime("%Y-%m-%d")
        return price, formatted_date
    except ValueError:
        return None, None

def scrape_car_data(car_model):
    """Scrape car data from Bring a Trailer based on the provided car model."""
    print(f"Starting scrape for car model: {car_model}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        print("WebDriver initialized successfully")

        driver.get("https://bringatrailer.com/")
        print("Navigated to Bring a Trailer")

        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/header/div/div[2]/div/form/div/bat-search-bar/div/input"))
        )
        search_bar.send_keys(car_model)
        print(f"Entered search term: {car_model}")

        search_bar.submit()
        print("Search submitted")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".listings-container.auctions-grid"))
        )

        while True:
            try:
                completed_auctions_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#auctions-completed-container > div.items-more > button"))
                )
                completed_auctions_button.click()
                print("Clicked 'Show More' for completed auctions")
                time.sleep(0.33)  # Using time to pause between clicks
            except Exception:
                print("No more 'Show More' buttons to click")
                break

        listings = driver.find_elements(By.CSS_SELECTOR, ".listings-container.auctions-grid .listing-card.bg-white-transparent")
        print(f"Found {len(listings)} listings")

        scraped_data = []
        for listing in listings:
            try:
                name = listing.find_element(By.CSS_SELECTOR, ".content-main h3").text
                details = listing.find_element(By.CSS_SELECTOR, ".content-main .item-results").text

                if "bid to" in details.lower():
                    continue

                year_match = re.search(r'\b(19[0-9]{2}|20[0-9]{2})\b', name)
                if not year_match:
                    continue

                year = year_match.group(0)
                price, auction_date = parse_listing_data(name, details)
                if price is None or auction_date is None:
                    continue

                scraped_data.append({
                    'year': year,
                    'price': f"${price:,.2f}",
                    'auction_date': auction_date
                })
                print(f"Scraped: {year} - ${price:,.2f} on {auction_date}")
            except Exception as e:
                print(f"Error processing a listing: {e}")

        print(f"Total records scraped: {len(scraped_data)}")
        return scraped_data

    except Exception as e:
        print(f"General error during scraping: {e}")
        return {"error": str(e)}

    finally:
        driver.quit()
        print("Driver quit successfully")

@app.route('/')
def home():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    """Endpoint to fetch car sales data."""
    try:
        car_model = request.json.get('car')
        if not car_model:
            return jsonify({"error": "Car model is required"}), 400

        data = scrape_car_data(car_model)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

