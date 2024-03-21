# Cars.com Scraper

This Python program allows you to scrape vehicle data from Cars.com based on specified criteria such as manufacturer and minimum year. It utilizes web scraping techniques to extract information about vehicles listed on Cars.com, including details such as name, price, features, and Carfax information.
## Prerequisites

Before running the program, ensure you have the following installed:

- Python 3
- Required Python libraries (requests, beautifulsoup4, tkinter)

You can install the required libraries using pip:

```pip install requests beautifulsoup4 tk```

## Usage

To use the program:

1. Clone or download the repository to your local machine.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the program files.
4. Run the program using the following command:

```python cars_com_scraper.py```

1. Enter the manufacturer, minimum year, and number of pages to scrape in the GUI window that appears.
2. Click the "Scrape" button to start scraping data.
3. The program will display the scraping progress in the text area and save the scraped data to a JSON file.

## Program Structure

The program consists of the following files:

- cars_com_scraper.py: The main Python script containing the scraping logic and GUI implementation.
- README.md: This README file providing information about the program.
- LICENSE: The license file for the program.

## Acknowledgments

This program is created for educational purposes and uses data from Cars.com. We acknowledge and thank Cars.com for providing the data used in this program.
