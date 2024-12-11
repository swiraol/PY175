import unittest
from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<ul>', response.get_data())

    def test_content(self):
        response = self.client.get('/history.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python was created in the late 1980s', response.get_data())

if __name__ == "__main__":
    unittest.main()
