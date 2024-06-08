import unittest
from models.country import Country


class TestCountry(unittest.TestCase):
    def setUp(self):
        self.country = Country(name="USA")

    def test_instance(self):
        self.assertIsInstance(self.country, Country)

    def test_name(self):
        self.assertEqual(self.country.name, "USA")

    def test_to_dict(self):
        country_dict = self.country.to_dict()
        self.assertEqual(country_dict["name"], "USA")
        self.assertEqual(country_dict["__class__"], "Country")


if __name__ == '__main__':
    unittest.main()
