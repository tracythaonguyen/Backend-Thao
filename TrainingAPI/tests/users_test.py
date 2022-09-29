from app.databases.mongodb import MongoDB
from app.models.user import User
from main import app
import json
import unittest

_db = MongoDB()


class UsersTests(unittest.TestCase):
    def test_register_users(self):
        body = json.dumps({
            "username": "tree",
            "password": "123"
        })
        request, response = app.test_client.post('/users/register', data=body)

        # delete user
        _db.delete_user({"username": "tree"})

        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.text).get("status"), "success")

    def test_register_users_user_exist(self):
        body = json.dumps({
            "username": "test",
            "password": "123"
        })
        request, response = app.test_client.post('/users/register', data=body)

        self.assertEqual(response.status, 400)
        self.assertEqual(json.loads(response.text).get('message'), "Bad Request: User exited")

    def test_login_users_no_exist(self):
        body = json.dumps({
            "username": "random",
            "password": "123"
        })
        request, response = app.test_client.post('/users/login', data=body)
        self.assertEqual(response.status, 404)

    def test_login_users_exist(self):
        body = json.dumps({
            "username": "test",
            "password": "123"
        })
        request, response = app.test_client.post('/users/login', data=body)
        self.assertEqual(response.status, 200)

    # error
    # def test_get_all_users_no_login(self):
    #     headers = {'Authorization': ''}
    #
    #     request, response = app.test_client.get('/users', headers=headers)
    #     self.assertEqual(response.status, 401)
    #     self.assertEqual(json.loads(response.text).get('message'), "Unauthorized: You are unauthorized.")

    def test_get_all_users_login(self):
        user = json.dumps({
            "username": "test",
            "password": "123"
        })
        request_user, response_user = app.test_client.post('/users/login', data=user)
        data = json.loads(response_user.text)
        token = data.get('token')
        headers = {'Authorization': token}

        request, response = app.test_client.get('/users', headers=headers)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_users'), 0)
        self.assertIsInstance(data.get('users'), list)


if __name__ == '__main__':
    unittest.main()
