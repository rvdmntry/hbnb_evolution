#!/usr/bin/python3


import unittest
from app import app

class UserEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user(self):
        response = self.app.post('/users', json={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_all_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        response = self.app.get('/users/<user_id>')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        response = self.app.put('/users/<user_id>', json={
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.app.delete('/users/<user_id>')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
