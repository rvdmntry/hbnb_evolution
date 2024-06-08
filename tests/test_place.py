import unittest
from models.place import Place


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.place = Place(
            name="Beach House",
            description="A lovely beach house.",
            address="123 Ocean Drive",
            city_id="SF",
            latitude=37.7749,
            longitude=-122.4194,
            host_id="host123",
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=200,
            max_guests=6
        )

    def test_instance(self):
        self.assertIsInstance(self.place, Place)

    def test_attributes(self):
        self.assertEqual(self.place.name, "Beach House")
        self.assertEqual(self.place.description, "A lovely beach house.")
        self.assertEqual(self.place.address, "123 Ocean Drive")
        self.assertEqual(self.place.city_id, "SF")
        self.assertEqual(self.place.latitude, 37.7749)
        self.assertEqual(self.place.longitude, -122.4194)
        self.assertEqual(self.place.host_id, "host123")
        self.assertEqual(self.place.number_of_rooms, 3)
        self.assertEqual(self.place.number_of_bathrooms, 2)
        self.assertEqual(self.place.price_per_night, 200)
        self.assertEqual(self.place.max_guests, 6)

    def test_to_dict(self):
        place_dict = self.place.to_dict()
        self.assertEqual(place_dict["name"], "Beach House")
        self.assertEqual(place_dict["city_id"], "SF")
        self.assertEqual(place_dict["__class__"], "Place")


if __name__ == '__main__':
    unittest.main()
