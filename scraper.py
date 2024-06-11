# scraper.py
import threading
import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Product
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraper:
    def __init__(self, base_url, pages):
        self.base_url = base_url
        self.pages = pages
        self.session = requests.Session()
        self.db_session = SessionLocal()

    def fetch_page(self, page_number):
        try:
            url = f"{self.base_url}?page={page_number}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page_number}: {e}")
            return None

    def parse_page(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        products = []
        for item in soup.select('.product-item'):
            try:
                name = item.select_one('.product-title').text.strip()
                price = float(item.select_one('.product-price').text.strip().replace('$', ''))
                rating = float(item.select_one('.product-rating').text.strip().replace(' stars', ''))
                reviews = int(item.select_one('.product-reviews').text.strip().replace(' reviews', ''))
                url = item.select_one('.product-link')['href']
                products.append(Product(name=name, price=price, rating=rating, reviews=reviews, url=url))
            except (AttributeError, ValueError) as e:
                logging.warning(f"Error parsing product: {e}")
        return products

    def save_products(self, products):
        try:
            self.db_session.add_all(products)
            self.db_session.commit()
        except Exception as e:
            logging.error(f"Error saving products to database: {e}")
            self.db_session.rollback()

    def scrape_page(self, page_number):
        html_content = self.fetch_page(page_number)
        if (html_content):
            products = self.parse_page(html_content)
            self.save_products(products)

    def run(self):
        threads = []
        for i in range(1, self.pages + 1):
            thread = threading.Thread(target=self.scrape_page, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.db_session.close()
