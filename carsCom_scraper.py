import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime

def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in ['-', '_', '.'] else '_' for c in filename)

def scrape_cars(page, total_pages):
    base_url = "https://www.cars.com/shopping/results/?"
    params = {
        "makes[]": "toyota",
        "year_min": 2019,
        "page_size": 20,
        "sort": "best_match_desc",
        "zip": "14202",
        "page": page  # This will iterate over different pages
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        car_listings = soup.find_all("div", class_="vehicle-card")
        scraped_data = []
        for car in car_listings:
            car_data = {}
            title_elem = car.find("h2", class_="title")
            car_data['title'] = title_elem.text.strip() if title_elem else "N/A"
            mileage_elem = car.find("div", class_="mileage")
            car_data['mileage'] = mileage_elem.text.strip() if mileage_elem else "N/A"
            price_elem = car.find("span", class_="primary-price")
            car_data['price'] = price_elem.text.strip() if price_elem else "N/A"
            dealer_name_elem = car.find("div", class_="dealer-name")
            car_data['dealer_name'] = dealer_name_elem.strong.text.strip() if dealer_name_elem else "N/A"
            image_elems = car.find_all("img", class_="vehicle-image")
            car_data['image_urls'] = [img['src'] for img in image_elems]
            scraped_data.append(car_data)
        
        # Write the scraped data to a JSON file
        sanitized_base_url = sanitize_filename(base_url)
        filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{sanitized_base_url}_page_{page}.json"
        with open(filename, "w") as f:
            json.dump(scraped_data, f, indent=4)
        
        # Print progress indicator
        print(f"Scraped page {page} of {total_pages} pages.")
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    total_pages = 5  # Total number of pages to scrape
    # Set up a loop to scrape multiple times
    for page in range(1, total_pages + 1):
        scrape_cars(page, total_pages)
        # Introduce a random delay between requests
        delay = random.uniform(2, 5)  # Random delay between 2 to 5 seconds
        time.sleep(delay)
