#!/usr/bin/python3


import unittest
import uuid
from models.user import User
from models.place import Place

class MockStorage:
    def __init__(self):
        self.users = {}
        self.places = {}

    def clear(self):
        self.users.clear()
        self.places.clear()

    def save_user(self, user):
        self.users[user.email] = user

    def get_user(self, email):
        return self.users.get(email)

    def save_place(self, place):
        self.places[place.id] = place

    def get_place(self, place_id):
        return self.places.get(place_id)

# Almacenamiento simulado global
storage = MockStorage()

class TestDataManager(unittest.TestCase):

    def setUp(self):
        # Limpiar el almacenamiento simulado y los correos electrónicos antes de cada prueba
        storage.clear()
        User.clear_emails()

    def test_save_and_get_user(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        storage.save_user(user)
        retrieved_user = storage.get_user("test@example.com")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_update_user(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        storage.save_user(user)
        user.update(first_name="Jane")
        storage.save_user(user)
        retrieved_user = storage.get_user("test@example.com")
        self.assertEqual(retrieved_user.first_name, "Jane")

    def test_save_and_get_place(self):
        place = Place(
            name="Lovely Apartment",
            description="A beautiful place",
            address="123 Main St",
            city_id=uuid.uuid4(),
            latitude=40.7128,
            longitude=-74.0060,
            host_id=uuid.uuid4(),
            number_of_rooms=2,
            number_of_bathrooms=1,
            price_per_night=150.0,
            max_guests=4,
            amenity_ids=[]
        )
        storage.save_place(place)
        retrieved_place = storage.get_place(place.id)
        self.assertIsNotNone(retrieved_place)
        self.assertEqual(retrieved_place.name, "Lovely Apartment")

if __name__ == '__main__':
    unittest.main()
