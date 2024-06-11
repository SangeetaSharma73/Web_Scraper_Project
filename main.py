# main.py
from scraper import WebScraper
from database import init_db

def main():
    init_db()
    base_url = "https://www.amazon.in/."
    pages = 10
    scraper = WebScraper(base_url, pages)
    scraper.run()

if __name__ == "__main__":
    main()
