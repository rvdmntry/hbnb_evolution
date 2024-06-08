import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    def setUp(self):
        self.amenity = Amenity(name="WiFi")

    def test_instance(self):
        self.assertIsInstance(self.amenity, Amenity)

    def test_name(self):
        self.assertEqual(self.amenity.name, "WiFi")

    def test_to_dict(self):
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict["name"], "WiFi")
        self.assertEqual(amenity_dict["__class__"], "Amenity")


if __name__ == '__main__':
    unittest.main()
