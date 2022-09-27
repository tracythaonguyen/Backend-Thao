from main import app
import json
import unittest


class BooksTests(unittest.TestCase):
    """ Unit testcases for REST APIs """

    def test_get_all_books(self):
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_books'), 0)
        self.assertIsInstance(data.get('books'), list)

    # TODO: unittest for another apis
    # def test_post_book_by_id(self):
    #     request, response = app.test_client.post('/books')
    #     self.assertEqual(response.status, 200)
    #     data = json.loads(response.text)
    #     self.assertEqual(data.get('status'), 'success')

    def test_get_book_by_id(self):
        request, response = app.test_client.get('/books/2ffa5b23-b279-45d1-b7ca-721209c216b7')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data.get('book'), object)

    # def test_put_book_by_id(self):
    #     request, response = app.test_client.put('/books/2ffa5b23-b279-45d1-b7ca-721209c216b7')
    #     self.assertEqual(response.status, 200)
    #     data = json.loads(response.text)
    #     self.assertEqual(data.get('status'), 'success')

    def test_delete_book_by_id(self):
        request, response = app.test_client.delete('/books/2ffa5b23-b279-45d1-b7ca-721209c216b7')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('status'), 'success')


if __name__ == '__main__':
    unittest.main()
