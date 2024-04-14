from RPA.Browser.Selenium import Selenium
import openpyxl
import requests
import logging
from datetime import datetime, timedelta

def scrape_news(search_phrase, news_category, num_months):
    # Initialize Selenium browser
    browser = Selenium()
    browser.open_available_browser("https://www.aljazeera.com/")

    try:
        # Input search phrase
        browser.input_text("xpath://input[@id='search-query']", search_phrase)
        browser.press_keys("xpath://input[@id='search-query']", "ENTER")
        browser.wait_until_page_contains_element("xpath://*[contains(@class,'latest-section')]")

        # Select news category if provided
        if news_category:
            browser.click_link(news_category)

        # Extract news articles based on time period
        current_date = datetime.now()
        for i in range(num_months + 1):
            target_date = current_date - timedelta(days=30 * i)
            formatted_date = target_date.strftime("%Y-%m-%d")
            browser.click_link(formatted_date)
            browser.wait_until_page_contains_element("xpath://*[contains(@class,'listing-type-news')]")

            titles = browser.get_webelements("xpath://*[contains(@class,'listing-type-news')]/h2/a")
            descriptions = browser.get_webelements("xpath://*[contains(@class,'listing-type-news')]/p")
            dates = browser.get_text("xpath://*[contains(@class,'listing-type-news')]/time")

            # Process and store news data
            process_news_data(titles, descriptions, dates)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        browser.close_browser()

def process_news_data(titles, descriptions, dates):
    # Create Excel workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Title'
    sheet['B1'] = 'Date'
    sheet['C1'] = 'Description'

    # Write news data to Excel
    for idx, (title, desc, date) in enumerate(zip(titles, descriptions, dates), start=2):
        sheet[f'A{idx}'] = title.text
        sheet[f'B{idx}'] = date
        sheet[f'C{idx}'] = desc.text if desc else ""

    # Save Excel file
    filename = 'news_data.xlsx'
    workbook.save(filename)
    logging.info(f"News data saved to {filename}")

if __name__ == "__main__":
    # Define parameters
    search_phrase = "Python"
    news_category = "Technology"  # Example: "Technology", "World News", etc.
    num_months = 2  # Extract news from the current month and previous two months

    # Execute news scraping
    scrape_news(search_phrase, news_category, num_months)
