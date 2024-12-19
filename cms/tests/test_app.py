import unittest
import shutil
import os
from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Explicitly set data path to 'tests/data' only once
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
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
    
    def admin_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'admin'
            return c

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
        self.create_document('changes.txt')
        client = self.admin_session()
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
    def test_updating_document_signed_out(self):
        response = self.client.post('/cms/data/changes.txt', data={'content': 'new content'})

        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("You must be signed in to do that.", follow_response.get_data(as_text=True))
    
    def test_view_new_document_form(self):
        client = self.admin_session()
        response = client.get('/cms/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn("<input name='filename'>", response.get_data(as_text=True))
        self.assertIn("<button type='submit'>", response.get_data(as_text=True))
    
    def test_view_new_document_form_signed_out(self):
        response = self.client.get('/cms/create')
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("You must be signed in to do that.", follow_response.get_data(as_text=True))

    def test_create_new_document(self):
        client = self.admin_session()
        response = client.post('/cms/create', data={'filename': 'test.txt'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("test.txt was created", response.get_data(as_text=True))

        response = self.client.get('/')
        self.assertIn('test.txt', response.get_data(as_text=True))
    
    def create_new_document_signed_out(self):
        response = self.client.post('/cms/create', data={'filename': 'test.txt'})
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("You must be signed in to do that.", follow_response.get_data(as_text=True))

    def test_create_new_document_without_filename(self):
        client = self.admin_session()
        response = client.post('/cms/create', data={'filename': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("A name is required.", response.get_data(as_text=True))
    
    def test_deleting_document(self):
        self.create_document('changes.txt')
        client = self.admin_session()
        response = client.post('/cms/data/changes.txt/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("changes.txt has been deleted.", response.get_data(as_text=True))
        self.assertFalse(os.path.exists(os.path.join(self.data_path, 'changes.txt')))
    
    def test_deleting_document_signed_out(self):
        self.create_document('test.txt')

        response = self.client.post('/test.txt/delete')
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("You must be signed in to do that.", follow_response.get_data(as_text=True))

    def test_signout(self):
        self.client.post('/users/signin', data={'username': 'admin', 'password': 'secret'})
        response = self.client.post('/users/signout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<a href='/users/signin'>Sign In</a>", response.get_data(as_text=True))
        self.assertIn('You have been signed out', response.get_data(as_text=True))
    def test_signin(self):
        response = self.client.post('/users/signin', data={'username': 'admin', 'password': 'secret'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.get_data(as_text=True))
        self.assertIn("Signed in as admin", response.get_data(as_text=True))

    def test_signin_with_bad_credentials(self):
        response = self.client.post('/users/signin', data={'username': 'invalid', 'password': 'invalid'}, follow_redirects=True)
        self.assertEqual(response.status_code, 422)
        self.assertIn('Invalid credentials', response.get_data(as_text=True))
        self.assertIn('value="invalid"', response.get_data(as_text=True))
    def test_signin_form(self):
        response = self.client.get('/users/signin')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<input name="username">', response.get_data(as_text=True))
        self.assertIn('<input name="password">', response.get_data(as_text=True))
        self.assertIn('<button type="submit">Sign In</button>', response.get_data(as_text=True))
    
    def test_edit_file_signed_out(self):
        self.create_document('test.txt', 'Test content')
        response = self.client.get('/cms/data/test.txt/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You must be signed in to do that.", response.get_data(as_text=True))
    
    def test_edit_file_signed_in(self):
        self.create_document('changes.txt', 'Initial content')
        client = self.admin_session()
        response = client.get('/cms/data/changes.txt/edit', follow_redirects=True)
        
        self.assertIn("<textarea name='content'>", response.get_data(as_text=True))
        self.assertIn("Initial content", response.get_data(as_text=True))
        self.assertIn('changes.txt', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
            


if __name__ == "__main__":
    unittest.main()

