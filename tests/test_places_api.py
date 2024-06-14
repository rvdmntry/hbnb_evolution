#!/usr/bin/python3


import unittest
import json
from api.places import app

class TestPlacesAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_place(self):
        place_data = {
            "name": "Beautiful Apartment",
            "description": "A lovely place to stay",
            "address": "123 Main St",
            "city_id": "some-city-id",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "host_id": "some-host-id",
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "price_per_night": 150.0,
            "max_guests": 4,
            "amenity_ids": ["some-amenity-id"]
        }
        response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.json)

    def test_get_places(self):
        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_place(self):
        place_data = {
            "name": "Cozy Cottage",
            "description": "A cozy place to relax",
            "address": "456 Elm St",
            "city_id": "some-city-id",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "host_id": "some-host-id",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 200.0,
            "max_guests": 6,
            "amenity_ids": ["some-amenity-id"]
        }
        post_response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        place_id = post_response.json['id']

        get_response = self.app.get(f'/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn('name', get_response.json)

    def test_update_place(self):
        place_data = {
            "name": "Modern Condo",
            "description": "A modern and sleek condo",
            "address": "789 Pine St",
            "city_id": "some-city-id",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "host_id": "some-host-id",
            "number_of_rooms": 1,
            "number_of_bathrooms": 1,
            "price_per_night": 300.0,
            "max_guests": 2,
            "amenity_ids": ["some-amenity-id"]
        }
        post_response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        place_id = post_response.json['id']

        update_data = {"name": "Modern and Spacious Condo"}
        put_response = self.app.put(f'/places/{place_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['name'], "Modern and Spacious Condo")

    def test_delete_place(self):
        place_data = {
            "name": "Rustic Cabin",
            "description": "A rustic cabin in the woods",
            "address": "321 Oak St",
            "city_id": "some-city-id",
            "latitude": 35.6895,
            "longitude": 139.6917,
            "host_id": "some-host-id",
            "number_of_rooms": 4,
            "number_of_bathrooms": 2,
            "price_per_night": 250.0,
            "max_guests": 8,
            "amenity_ids": ["some-amenity-id"]
        }
        post_response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        place_id = post_response.json['id']

        delete_response = self.app.delete(f'/places/{place_id}')
        self.assertEqual(delete_response.status_code, 204)

        get_response = self.app.get(f'/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
