import logging
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from scraper import search_news, extract_articles, process_news_data
from utils import init_browser
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')

def scrape_news(search_phrase, num_months=0):
    """Main function to scrape news based on search phrase."""
    browser = init_browser()

    try:
        search_news(browser, search_phrase)
        target_date = datetime.now() - timedelta(days=30 * num_months)
        articles = extract_articles(browser, target_date)
        process_news_data(articles, target_date, search_phrase)
        logging.info(f"Scraping {search_phrase} completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    finally:
        browser.quit()
        logging.info("Cleaning up completed.")

if __name__ == "__main__":
    search_phrase = "USD"
    scrape_news(search_phrase, num_months=1)
