import unittest
from models.place import Place
from models.user import User
from models.city import City


class TestPlace(unittest.TestCase):
    def test_create_place(self):
        user = User(email="host@example.com", password="password",
                    first_name="Jane", last_name="Smith")
        city = City(name="New York", country=None)
        place = Place(name="Cozy Cottage", description="A nice little cottage", address="123 Main St", city=city,
                      latitude=40.7128, longitude=-74.0060, host=user, number_of_rooms=3, bathrooms=2, price_per_night=150, max_guests=5)
        self.assertIsNotNone(place.id)
        self.assertEqual(place.name, "Cozy Cottage")
        self.assertEqual(place.city.name, "New York")


if __name__ == '__main__':
    unittest.main()
