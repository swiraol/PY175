import unittest
import shutil
import os

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Explicitly set data path to 'tests/data' only once
        self.data_path = os.path.join(os.path.dirname(__file__), 'tests', 'data')
        os.makedirs(self.data_path, exist_ok=True)

        # Debug output to confirm path correctness
        # print(f"SetUp: Data path set to {self.data_path}")



    def tearDown(self):
        # print(f"TearDown: Removing directory {self.data_path}")  # Debugging
        shutil.rmtree(self.data_path, ignore_errors=True)
        # print(f"TearDown: Directory removed.")  # Debugging

    
    def create_document(self, name, content=''):
        file_path = os.path.join(self.data_path, name)
        # print(f"Creating file at: {file_path}")  # Debugging
        with open(file_path, 'w') as file:
            file.write(content)

    def test_index(self):
        self.create_document('about.md')
        self.create_document('changes.txt')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertIn('/cms/data/about.md', response.get_data(as_text=True))
        self.assertIn('/cms/data/changes.txt', response.get_data(as_text=True))
        self.assertIn(b"<ul>", response.get_data())

    def test_content(self):
        self.create_document('history.txt', 'Python 0.9.0 (initial release) is released.')
        response = self.client.get('/cms/data/history.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/plain; charset=utf-8')
        self.assertIn("Python 0.9.0 (initial release) is released.", response.get_data(as_text=True))

    def test_nonexistent_file(self):
        with self.client.get('/cms/data/history1.txt') as response:
            self.assertEqual(response.status_code, 302)

        with self.client.get(response.headers['Location']) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"history1.txt does not exist", response.data,)
    def test_markdown_file(self):
        self.create_document('about.md', '# This is my app.')
        response = self.client.get('/cms/data/about.md')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>This is my app.</h1>", response.data)
        
    def test_updating_document(self):
        response = self.client.post("/cms/data/changes.txt",
                                    data={'content': "new content"})
        self.assertEqual(response.status_code, 302)

        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("changes.txt has been updated",
                      follow_response.get_data(as_text=True))

        with self.client.get("/cms/data/changes.txt") as content_response:
            self.assertEqual(content_response.status_code, 200)
            self.assertIn("new content",
                          content_response.get_data(as_text=True))
    
    def test_view_new_document_form(self):
        response = self.client.get('/cms/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn("<input name='filename'>", response.get_data(as_text=True))
        self.assertIn("<button type='submit'>", response.get_data(as_text=True))

    def test_create_new_document(self):
        response =self.client.post('/cms/create', data={'filename': 'test.txt'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("test.txt was created", response.get_data(as_text=True))

        response = self.client.get('/')
        self.assertIn('test.txt', response.get_data(as_text=True))

    def test_create_new_document_without_filename(self):
        response = self.client.post('/cms/create', data={'filename': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("A name is required.", response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()

