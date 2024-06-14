#!/usr/bin/python3


import unittest
from model.user.py import User

class TestUser(unittest.TestCase):

    def setUp(self):
        User.emails = set()

    def test_user_creation(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_duplicate_email(self):
        user1 = User(email="test@example.com", first_name="John", last_name="Doe")
        with self.assertRaises(ValueError):
            user2 = User(email="test@example.com", first_name="Jane", last_name="Doe")

if __name__ == "__main__":
    unittest.main()
