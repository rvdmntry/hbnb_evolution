import unittest
from models.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        # Reset the data manager's object store for isolation
        User.data_manager.__objects = {}
        self.user = User(email="test@example.com", password="password123")

    def test_instance(self):
        self.assertIsInstance(self.user, User)

    def test_attributes(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["email"], "test@example.com")
        self.assertEqual(user_dict["__class__"], "User")

    def test_unique_email(self):
        with self.assertRaises(ValueError):
            User(email="test@example.com", password="newpassword")


if __name__ == '__main__':
    unittest.main()
