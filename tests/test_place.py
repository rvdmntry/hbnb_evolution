#!/usr/bin/python3
import unittest
import json
from app import app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.city_data = {
            'name': 'Test City',
            'country_code': 'US'
        }
        self.city_response = self.client.post(
            '/cities', data=json.dumps(self.city_data), content_type='application/json')
        self.city_id = self.city_response.json['id']
        self.amenity_data = {
            'name': 'Test Amenity'
        }
        self.amenity_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        self.amenity_id = self.amenity_response.json['id']
        self.place_data = {
            'name': 'Test Place',
            'description': 'A place for testing',
            'address': '123 Test St',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': 'test-host',
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 100.0,
            'max_guests': 4,
            'amenity_ids': [self.amenity_id]
        }

    def tearDown(self):
        # Clean up test data
        import shutil
        shutil.rmtree('data/places', ignore_errors=True)
        shutil.rmtree('data/cities', ignore_errors=True)
        shutil.rmtree('data/amenities', ignore_errors=True)

    def test_create_place(self):
        response = self.client.post(
            '/places', data=json.dumps(self.place_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_places(self):
        self.client.post('/places', data=json.dumps(self.place_data),
                         content_type='application/json')
        response = self.client.get('/places')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_place(self):
        post_response = self.client.post(
            '/places', data=json.dumps(self.place_data), content_type='application/json')
        place_id = post_response.json['id']
        get_response = self.client.get(f'/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['name'], self.place_data['name'])

    def test_update_place(self):
        post_response = self.client.post(
            '/places', data=json.dumps(self.place_data), content_type='application/json')
        place_id = post_response.json['id']
        updated_data = {
            'name': 'Updated Place',
            'description': 'An updated place for testing',
            'address': '456 Test Ave',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': 'test-host',
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.0,
            'max_guests': 6,
            'amenity_ids': [self.amenity_id]
        }
        put_response = self.client.put(
            f'/places/{place_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['name'], 'Updated Place')

    def test_delete_place(self):
        post_response = self.client.post(
            '/places', data=json.dumps(self.place_data), content_type='application/json')
        place_id = post_response.json['id']
        delete_response = self.client.delete(f'/places/{place_id}')
        self.assertEqual(delete_response.status_code, 204)
        get_response = self.client.get(f'/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
