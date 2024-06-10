import unittest
from models.user import User


class TestUser(unittest.TestCase):
    def test_create_user(self):
        user = User(email="test@example.com", password="password",
                    first_name="John", last_name="Doe")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")


if __name__ == '__main__':
    unittest.main()
