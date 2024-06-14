#!/usr/bin/python3


import unittest
from model.place import Place

class TestPlace(unittest.TestCase):

    def test_place_creation(self):
        place = Place(host_id=uuid.uuid4(), name="Lovely Apartment", description="A beautiful place", number_of_rooms=2, number_of_bathrooms=1, max_guests=4, price_per_night=150.0, latitude=40.7128, longitude=-74.0060, city_id=uuid.uuid4(), amenity_ids=[])
        self.assertEqual(place.name, "Lovely Apartment")
        self.assertEqual(place.number_of_rooms, 2)

if __name__ == "__main__":
    unittest.main()
