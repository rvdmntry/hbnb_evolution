import unittest
import os
from models.user import User
from persistence.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.user = User(email="unique@example.com", password="password123")
        FileStorage.__file_path = "test_file.json"
        FileStorage.__objects = {}

    def tearDown(self):
        try:
            os.remove("test_file.json")
        except FileNotFoundError:
            pass

    def test_save_and_load(self):
        FileStorage.save(self.user)
        FileStorage.load()
        retrieved_user = FileStorage.get(self.user.id)
        self.assertEqual(retrieved_user["email"], "unique@example.com")
        self.assertEqual(retrieved_user["password"], "password123")
        self.assertEqual(retrieved_user["__class__"], "User")


if __name__ == '__main__':
    unittest.main()
