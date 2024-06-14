#!/usr/bin/python3


import unittest
import json
from api.users import app

class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user(self):
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('email', response.json)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        user_data = {
            "email": "test2@example.com",
            "first_name": "Jane",
            "last_name": "Doe"
        }
        post_response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        user_id = post_response.json['id']

        get_response = self.app.get(f'/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn('email', get_response.json)

    def test_update_user(self):
        user_data = {
            "email": "test3@example.com",
            "first_name": "Jim",
            "last_name": "Beam"
        }
        post_response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        user_id = post_response.json['id']

        update_data = {
            "email": "test3_updated@example.com",
            "first_name": "Jimmy",
            "last_name": "Beam"
        }
        put_response = self.app.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['email'], "test3_updated@example.com")

    def test_delete_user(self):
        user_data = {
            "email": "test4@example.com",
            "first_name": "Jack",
            "last_name": "Daniels"
        }
        post_response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        user_id = post_response.json['id']

        delete_response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(delete_response.status_code, 204)

        get_response = self.app.get(f'/users/{user_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

