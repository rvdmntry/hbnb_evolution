#!/usr/bin/python3
import unittest
from models.user import User


class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = User(email="test@example.com", password="password",
                    first_name="Test", last_name="User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_user_to_dict(self):
        user = User(email="test@example.com", password="password",
                    first_name="Test", last_name="User")
        user_dict = user.to_dict()
        self.assertEqual(user_dict['email'], "test@example.com")
        self.assertEqual(user_dict['first_name'], "Test")
        self.assertEqual(user_dict['last_name'], "User")
        self.assertEqual(user_dict['password'], "password")
        self.assertIsNotNone(user_dict['id'])
        self.assertIsNotNone(user_dict['created_at'])
        self.assertIsNotNone(user_dict['updated_at'])


if __name__ == '__main__':
    unittest.main()
