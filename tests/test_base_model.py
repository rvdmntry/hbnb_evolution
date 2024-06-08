import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.base = BaseModel()

    def test_instance(self):
        self.assertIsInstance(self.base, BaseModel)

    def test_id(self):
        self.assertIsInstance(self.base.id, str)
        self.assertEqual(len(self.base.id), 36)

    def test_created_at(self):
        self.assertIsInstance(self.base.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_to_dict(self):
        base_dict = self.base.to_dict()
        self.assertIsInstance(base_dict, dict)
        self.assertEqual(base_dict["__class__"], "BaseModel")
        self.assertIn("created_at", base_dict)
        self.assertIn("updated_at", base_dict)

    def test_save(self):
        old_updated_at = self.base.updated_at
        self.base.save()
        self.assertNotEqual(self.base.updated_at, old_updated_at)


if __name__ == '__main__':
    unittest.main()
