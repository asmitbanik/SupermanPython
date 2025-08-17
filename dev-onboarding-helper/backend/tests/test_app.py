import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_ask(self):
        response = self.client.post('/api/ask', json={'question': 'Hello?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.get_json())

if __name__ == '__main__':
    unittest.main()
