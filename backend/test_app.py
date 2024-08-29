import unittest
from unittest.mock import patch, MagicMock
from app import app, extract_isbn, google_search_isbn, extract_asin_from_url, find_asin_in_results, call_amazon_api

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.client.text_detection')
    def test_upload_file_success(self, mock_text_detection):
        mock_text_detection.return_value = MagicMock(text_annotations=[MagicMock(description='ISBN 9781234567890')])
        
        with patch('app.google_search_isbn') as mock_google_search:
            mock_google_search.return_value = ['https://www.amazon.com/dp/B00EXAMPLE']
            
            with patch('app.call_amazon_api') as mock_call_amazon_api:
                mock_call_amazon_api.return_value = {
                    'data': {
                        'amazonProduct': {
                            'title': 'Example Book',
                            'price': {'display': '$10.00'},
                            'mainImageUrl': 'http://example.com/image.png'
                        }
                    }
                }
                file_data = {
                    'file': (open('test_image.png', 'rb'), 'test_image.png')
                }
                response = self.app.post('/api/upload', data=file_data, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Example Book', response.data)
                self.assertIn(b'9781234567890', response.data)
                self.assertIn(b'B00EXAMPLE', response.data)
                self.assertIn(b'$10.00', response.data)

    @patch('app.client.text_detection')
    def test_upload_file_no_isbn_found(self, mock_text_detection):
        mock_text_detection.return_value = MagicMock(text_annotations=[])
        file_data = {
            'file': (open('test_image.png', 'rb'), 'test_image.png')
        }
        response = self.app.post('/api/upload', data=file_data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No ISBN found in the text', response.data)

    def test_extract_isbn(self):
        text = "ISBN 978-3-16-148410-0"
        isbn = extract_isbn(text)
        self.assertEqual(isbn, "9783161484100")

    @patch('app.search')
    def test_google_search_isbn(self, mock_search):
        mock_search.return_value = ['https://www.amazon.com/dp/B00EXAMPLE']
        search_results = google_search_isbn("9783161484100")
        self.assertIn('https://www.amazon.com/dp/B00EXAMPLE', search_results)

    def test_extract_asin_from_url(self):
        url = "https://www.amazon.com/dp/B00EXAMPLE"
        asin = extract_asin_from_url(url)
        self.assertEqual(asin, "B00EXAMPLE")

    def test_find_asin_in_results(self):
        search_results = [
            "https://www.notamazon.com/product/123456",
            "https://www.amazon.com/dp/B00EXAMPLE"
        ]
        asin = find_asin_in_results(search_results)
        self.assertEqual(asin, "B00EXAMPLE")

    @patch('requests.post')
    def test_call_amazon_api_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'data': {
                'amazonProduct': {
                    'title': 'Example Book',
                    'price': {'display': '$10.00'},
                    'mainImageUrl': 'http://example.com/image.png'
                }
            }
        }
        asin = "B00EXAMPLE"
        response = call_amazon_api(asin)
        self.assertIn('amazonProduct', response['data'])
        self.assertEqual(response['data']['amazonProduct']['title'], 'Example Book')

    @patch('requests.post')
    def test_call_amazon_api_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        asin = "B00EXAMPLE"
        response = call_amazon_api(asin)
        self.assertIn('error', response)
        self.assertEqual(response['error'], 'Failed to fetch data from Canopy API')


if __name__ == '__main__':
    unittest.main()