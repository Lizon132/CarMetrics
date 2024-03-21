import json
import random
import time
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def get_vehicle_list(manufacturer, min_year, pages_to_scrape):
    vehicle_list = []

    for page in range(1, pages_to_scrape + 1):
        url = f"https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]={manufacturer}&maximum_distance=30&mileage_max=&monthly_payment=&page_size=20&sort=best_match_desc&stock_type=all&year_max=&year_min={min_year}&zip=14202&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='vehicle-card')
            for result in results:
                vehicle = {}
                url_element = result.find('a', class_='vehicle-card-link')
                if url_element:
                    vehicle['url'] = url_element.get('href')
                    vehicle['name'] = url_element.find('h2', class_='title').text.strip()
                else:
                    vehicle['name'] = "N/A"
                    vehicle['url'] = "N/A"

                price_element = result.find('span', class_='primary-price')
                if price_element:
                    vehicle['price'] = price_element.text.strip()
                else:
                    vehicle['price'] = "N/A"

                vehicle_list.append(vehicle)
        else:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")

    return vehicle_list



def scrape_vehicle_details(vehicle, text_widget):
    url = f"https://www.cars.com{vehicle['url']}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        details = {}
        
        # Scrape features section
        features_section = soup.find('section', class_='features-section')
        if features_section:
            features_list = features_section.find_all('ul', class_='vehicle-features-list')
            for feature_list in features_list:
                category_element = feature_list.find_previous_sibling('dt')
                if category_element:
                    category = category_element.text.strip()
                    features = [li.text.strip() for li in feature_list.find_all('li')]
                    details[category] = features
        
        # Scrape basics section
        basics_section = soup.find('section', class_='basics-section')
        if basics_section:
            basics_list = basics_section.find('dl', class_='fancy-description-list')
            if basics_list:
                for dt, dd in zip(basics_list.find_all('dt'), basics_list.find_all('dd')):
                    details[dt.text.strip()] = dd.text.strip()
        
        # Scrape Carfax information
        carfax_info = soup.find('dl', class_='fancy-description-list')
        if carfax_info:
            carfax_info = carfax_info.find_all('dd')
            details['accidents_or_damage'] = carfax_info[0].text.strip() if len(carfax_info) > 0 else "N/A"
            details['one_owner'] = carfax_info[1].text.strip() if len(carfax_info) > 1 else "N/A"
            details['personal_use'] = carfax_info[2].text.strip() if len(carfax_info) > 2 else "N/A"
            details['open_recall'] = carfax_info[3].text.strip() if len(carfax_info) > 3 else "N/A"
        else:
            details['accidents_or_damage'] = "N/A"
            details['one_owner'] = "N/A"
            details['personal_use'] = "N/A"
            details['open_recall'] = "N/A"

        vehicle.update(details)
        text_widget.insert(tk.END, f"Scraped details for: {vehicle['name']}\n")
    else:
        text_widget.insert(tk.END, f"Failed to fetch details for: {vehicle['name']}. Status code: {response.status_code}\n")

    return vehicle



def scrape_and_save(manufacturer, min_year, pages_to_scrape, text_widget):
    vehicle_list = get_vehicle_list(manufacturer, min_year, pages_to_scrape)

    scraped_data = []
    for vehicle in vehicle_list:
        text_widget.insert(tk.END, f"Scraping details for: {vehicle['name']}\n")
        time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds
        vehicle = scrape_vehicle_details(vehicle, text_widget)
        scraped_data.append(vehicle)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"cars_data_{timestamp}.json"
    with open(filename, 'w') as file:
        json.dump(scraped_data, file, indent=4)

    text_widget.insert(tk.END, f"\nScraping complete. Data saved to: {filename}\n")

class CarsScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cars.com Scraper")

        self.manufacturer_label = ttk.Label(self, text="Manufacturer:")
        self.manufacturer_entry = ttk.Entry(self, width=30)

        self.min_year_label = ttk.Label(self, text="Min Year:")
        self.min_year_entry = ttk.Entry(self, width=10)

        self.pages_label = ttk.Label(self, text="Pages to Scrape:")
        self.pages_entry = ttk.Entry(self, width=10)

        self.submit_button = ttk.Button(self, text="Scrape", command=self.on_submit)

        self.text_widget = tk.Text(self, wrap="word", height=20, width=70)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.manufacturer_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.manufacturer_entry.grid(row=0, column=1, padx=10, pady=5)
        self.min_year_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.min_year_entry.grid(row=1, column=1, padx=10, pady=5)
        self.pages_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.pages_entry.grid(row=2, column=1, padx=10, pady=5)
        self.submit_button.grid(row=3, columnspan=2, pady=10)
        self.text_widget.grid(row=4, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.scrollbar.grid(row=4, column=2, sticky="ns")

    def on_submit(self):
        manufacturer = self.manufacturer_entry.get().strip()
        min_year = self.min_year_entry.get().strip()
        pages_to_scrape = int(self.pages_entry.get().strip())

        scrape_and_save(manufacturer, min_year, pages_to_scrape, self.text_widget)


if __name__ == "__main__":
    app = CarsScraperApp()
    app.mainloop()
