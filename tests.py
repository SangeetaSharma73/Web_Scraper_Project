# tests.py
import unittest
from scraper import WebScraper
from unittest.mock import patch

class TestWebScraper(unittest.TestCase):
    @patch('scraper.requests.get')
    def test_fetch_page(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html></html>'
        scraper = WebScraper('http://example.com', 1)
        content = scraper.fetch_page(1)
        self.assertEqual(content, '<html></html>')

    @patch('scraper.WebScraper.save_products')
    def test_parse_page(self, mock_save):
        html_content = """
        <div class="product-item">
            <div class="product-title">Test Product</div>
            <div class="product-price">$19.99</div>
            <div class="product-rating">4.5 stars</div>
            <div class="product-reviews">10 reviews</div>
            <a class="product-link" href="http://example.com/product/1"></a>
        </div>
        """
        scraper = WebScraper('http://example.com', 1)
        products = scraper.parse_page(html_content)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, 'Test Product')
        self.assertEqual(products[0].price, 19.99)
        self.assertEqual(products[0].rating, 4.5)
        self.assertEqual(products[0].reviews, 10)
        self.assertEqual(products[0].url, 'http://example.com/product/1')

if __name__ == '__main__':
    unittest.main()
