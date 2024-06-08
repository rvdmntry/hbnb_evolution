import unittest
from models.city import City


class TestCity(unittest.TestCase):
    def setUp(self):
        self.city = City(name="San Francisco", country_id="USA")

    def test_instance(self):
        self.assertIsInstance(self.city, City)

    def test_attributes(self):
        self.assertEqual(self.city.name, "San Francisco")
        self.assertEqual(self.city.country_id, "USA")

    def test_to_dict(self):
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict["name"], "San Francisco")
        self.assertEqual(city_dict["country_id"], "USA")
        self.assertEqual(city_dict["__class__"], "City")


if __name__ == '__main__':
    unittest.main()
